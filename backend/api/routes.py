from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from typing import List

from db.database import get_db
from db import crud
from api import schemas
from ai.stt import mock_speech_to_text
from ai.llm import extract_intent_mock
from engine.validation import validate_intent
from engine.rules import execute_business_rules
from engine.resolver import resolve_inventory_item
from engine.audit import log_action
import os
import shutil

router = APIRouter()

@router.post("/voice")
async def process_voice_command(audio: UploadFile = File(...), db: Session = Depends(get_db)):
    # 0. Audio Handling: Save file locally
    os.makedirs("uploads", exist_ok=True)
    file_path = f"uploads/{audio.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(audio.file, buffer)
        
    # 1. STT
    transcription = mock_speech_to_text(file_path)
    
    # 2. LLM Intent
    intent_data = extract_intent_mock(transcription)
    
    # 3. Validation Layer
    is_valid, err = validate_intent(intent_data)
    if not is_valid:
        log_action(db, "Validation Failed", intent_data)
        raise HTTPException(status_code=400, detail=err)
        
    # 3.5 Resolver: Resolve item names to actual DB items
    if intent_data.get("intent") == "Record Sale":
        for item in intent_data.get("items", []):
            resolved_item = resolve_inventory_item(db, item.get("name"))
            if resolved_item:
                item["resolved_id"] = resolved_item.id
                item["name"] = resolved_item.name # Normalize name
            else:
                log_action(db, "Resolver Failed", intent_data)
                raise HTTPException(status_code=400, detail=f"Could not resolve item: {item.get('name')}")
                
    # 4. Business Rules
    is_allowed, rule_err, warnings = execute_business_rules(db, intent_data)
    if not is_allowed:
        log_action(db, "Business Rules Failed", intent_data)
        raise HTTPException(status_code=400, detail=rule_err)
        
    # 5. DB Transaction Execution
    execution_result = {}
    intent = intent_data.get("intent")
    
    if intent == "Record Sale":
        for item in intent_data.get("items", []):
            sale = schemas.SaleCreate(
                inventory_id=item["resolved_id"],
                quantity=item["quantity"],
                total_price=intent_data.get("total_price", 0),
                discount=intent_data.get("discount", 0.0),
                is_override=intent_data.get("is_override", 0)
            )
            crud.create_sale(db, sale)
        execution_result = {"message": "Sale recorded successfully."}
        
    elif intent == "Restock" or intent == "Record Purchase":
        for item in intent_data.get("items", []):
            purchase = schemas.PurchaseCreate(
                inventory_id=item["resolved_id"],
                quantity=item["quantity"],
                cost_price=item.get("cost_price", 0)
            )
            crud.create_purchase(db, purchase)
        execution_result = {"message": "Restock recorded successfully."}
        
    elif intent == "Delete Item":
        item_name = intent_data.get("name")
        resolved = resolve_inventory_item(db, item_name)
        if resolved and resolved[0]:
            crud.delete_inventory_item(db, resolved[0].id)
            execution_result = {"message": f"Deleted {item_name} from inventory."}
            
    elif intent == "Inventory Query":
        item_name = intent_data.get("name")
        resolved = resolve_inventory_item(db, item_name)
        if resolved and resolved[0]:
            execution_result = {"message": f"You have {resolved[0].quantity} {resolved[0].name} left."}
            
    elif intent == "Profit Query":
        profit = crud.get_profit_report(db)
        execution_result = {"message": f"Total profit is {profit['profit']}."}
        
    log_action(db, "Success", intent_data)
    
    return {
        "status": "success", 
        "transcription": transcription, 
        "intent": intent_data,
        "warnings": warnings,
        "execution": execution_result
    }

# --- INVENTORY ROUTES ---
@router.post("/inventory/", response_model=schemas.InventoryResponse)
def create_inventory_item(item: schemas.InventoryCreate, db: Session = Depends(get_db)):
    db_item = crud.get_inventory_item_by_name(db, name=item.name)
    if db_item:
        raise HTTPException(status_code=400, detail="Item already exists")
    return crud.create_inventory_item(db=db, item=item)

@router.get("/inventory/", response_model=List[schemas.InventoryResponse])
def read_inventory(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_inventory(db, skip=skip, limit=limit)
    return items

@router.put("/inventory/{item_id}", response_model=schemas.InventoryResponse)
def update_inventory_item(item_id: int, item: schemas.InventoryUpdate, db: Session = Depends(get_db)):
    db_item = crud.update_inventory_item(db, item_id, item)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@router.delete("/inventory/{item_id}")
def delete_inventory_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.delete_inventory_item(db, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"status": "success", "message": "Item deleted"}

# --- CUSTOMER ROUTES ---
@router.post("/customers/", response_model=schemas.CustomerResponse)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    return crud.create_customer(db=db, customer=customer)

@router.get("/customers/", response_model=List[schemas.CustomerResponse])
def read_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_customers(db, skip=skip, limit=limit)

# --- SALES ROUTES ---
@router.post("/sales/", response_model=schemas.SaleResponse)
def create_sale(sale: schemas.SaleCreate, db: Session = Depends(get_db)):
    db_item = crud.get_inventory_item(db, sale.inventory_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    if db_item.quantity < sale.quantity:
        raise HTTPException(status_code=400, detail="Not enough inventory")
    return crud.create_sale(db=db, sale=sale)

@router.get("/sales/", response_model=List[schemas.SaleResponse])
def read_sales(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_sales(db, skip=skip, limit=limit)

# --- PURCHASES / RESTOCK ROUTES ---
@router.post("/purchases/", response_model=schemas.PurchaseResponse)
def create_purchase(purchase: schemas.PurchaseCreate, db: Session = Depends(get_db)):
    db_item = crud.get_inventory_item(db, purchase.inventory_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    return crud.create_purchase(db=db, purchase=purchase)

@router.get("/purchases/", response_model=List[schemas.PurchaseResponse])
def read_purchases(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_purchases(db, skip=skip, limit=limit)

# --- TRANSACTIONS ROUTES ---
@router.post("/transactions/", response_model=schemas.TransactionResponse)
def create_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    db_customer = crud.get_customer(db, transaction.customer_id)
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return crud.create_transaction(db=db, transaction=transaction)

@router.get("/transactions/", response_model=List[schemas.TransactionResponse])
def read_transactions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_transactions(db, skip=skip, limit=limit)

# --- EMPLOYEES ROUTES ---
@router.post("/employees/", response_model=schemas.EmployeeResponse)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    db_user = crud.get_employee_by_username(db, username=employee.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_employee(db=db, employee=employee)

# --- SETTINGS ROUTES ---
@router.post("/settings/", response_model=schemas.SettingResponse)
def set_setting(setting: schemas.SettingCreate, db: Session = Depends(get_db)):
    return crud.set_setting(db=db, setting=setting)

@router.get("/settings/{key}")
def get_setting(key: str, db: Session = Depends(get_db)):
    db_setting = crud.get_setting(db, key=key)
    if db_setting is None:
        raise HTTPException(status_code=404, detail="Setting not found")
    return {"key": db_setting.key, "value": db_setting.value}

# --- REPORTS ROUTES ---
@router.get("/reports/daily")
def get_daily_report(db: Session = Depends(get_db)):
    return crud.get_daily_report(db)

@router.get("/reports/profit")
def get_profit_report(db: Session = Depends(get_db)):
    return crud.get_profit_report(db)
