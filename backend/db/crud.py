from sqlalchemy.orm import Session
from . import models
from api import schemas

# --- INVENTORY CRUD ---
def get_inventory_item(db: Session, item_id: int):
    return db.query(models.Inventory).filter(models.Inventory.id == item_id).first()

def get_inventory_item_by_name(db: Session, name: str):
    return db.query(models.Inventory).filter(models.Inventory.name == name).first()

def get_inventory(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Inventory).offset(skip).limit(limit).all()

def create_inventory_item(db: Session, item: schemas.InventoryCreate):
    db_item = models.Inventory(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_inventory_item(db: Session, item_id: int, item_update: schemas.InventoryUpdate):
    db_item = db.query(models.Inventory).filter(models.Inventory.id == item_id).first()
    if db_item:
        update_data = item_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_item, key, value)
        db.commit()
        db.refresh(db_item)
    return db_item

def delete_inventory_item(db: Session, item_id: int):
    db_item = db.query(models.Inventory).filter(models.Inventory.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item

# --- CUSTOMER CRUD ---
def get_customer(db: Session, customer_id: int):
    return db.query(models.Customer).filter(models.Customer.id == customer_id).first()

def get_customers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Customer).offset(skip).limit(limit).all()

def create_customer(db: Session, customer: schemas.CustomerCreate):
    db_customer = models.Customer(**customer.model_dump())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

# --- SALES CRUD ---
def create_sale(db: Session, sale: schemas.SaleCreate):
    try:
        db_sale = models.Sale(**sale.model_dump())
        db.add(db_sale)
        
        # Also deduct from inventory
        db_item = db.query(models.Inventory).filter(models.Inventory.id == sale.inventory_id).first()
        if db_item:
            db_item.quantity -= sale.quantity
            
        db.commit()
        db.refresh(db_sale)
        return db_sale
    except Exception as e:
        db.rollback()
        raise e

def get_sales(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Sale).offset(skip).limit(limit).all()

# --- PURCHASES CRUD ---
def create_purchase(db: Session, purchase: schemas.PurchaseCreate):
    try:
        db_purchase = models.Purchase(**purchase.model_dump())
        db.add(db_purchase)
        
        db_item = db.query(models.Inventory).filter(models.Inventory.id == purchase.inventory_id).first()
        if db_item:
            db_item.quantity += purchase.quantity
            
        db.commit()
        db.refresh(db_purchase)
        return db_purchase
    except Exception as e:
        db.rollback()
        raise e

def get_purchases(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Purchase).offset(skip).limit(limit).all()

# --- TRANSACTIONS CRUD ---
def create_transaction(db: Session, transaction: schemas.TransactionCreate):
    try:
        db_transaction = models.Transaction(**transaction.model_dump())
        db.add(db_transaction)
        
        db_customer = db.query(models.Customer).filter(models.Customer.id == transaction.customer_id).first()
        if db_customer:
            if transaction.transaction_type == "credit":
                db_customer.credit_balance += transaction.amount
            elif transaction.transaction_type == "payment":
                db_customer.credit_balance -= transaction.amount
                
        db.commit()
        db.refresh(db_transaction)
        return db_transaction
    except Exception as e:
        db.rollback()
        raise e

def get_transactions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Transaction).offset(skip).limit(limit).all()

# --- SETTINGS CRUD ---
def get_setting(db: Session, key: str):
    return db.query(models.Setting).filter(models.Setting.key == key).first()

def set_setting(db: Session, setting: schemas.SettingCreate):
    db_setting = db.query(models.Setting).filter(models.Setting.key == setting.key).first()
    if db_setting:
        db_setting.value = setting.value
    else:
        db_setting = models.Setting(key=setting.key, value=setting.value)
        db.add(db_setting)
    db.commit()
    db.refresh(db_setting)
    return db_setting

# --- EMPLOYEES CRUD ---
def create_employee(db: Session, employee: schemas.EmployeeCreate):
    # In a real app, hash the password here (e.g., using passlib)
    hashed_pwd = employee.password + "_hashed" # Mock hashing
    db_emp = models.Employee(username=employee.username, hashed_password=hashed_pwd, role=employee.role)
    db.add(db_emp)
    db.commit()
    db.refresh(db_emp)
    return db_emp

def get_employee_by_username(db: Session, username: str):
    return db.query(models.Employee).filter(models.Employee.username == username).first()

# --- REPORTS CRUD ---
from sqlalchemy import func
from datetime import datetime, timedelta

def get_daily_report(db: Session):
    today = datetime.now().date()
    sales = db.query(
        func.sum(models.Sale.total_price).label("total_revenue"),
        func.count(models.Sale.id).label("transactions_count")
    ).filter(func.date(models.Sale.created_at) == today).first()
    
    return {
        "date": str(today),
        "total_revenue": sales.total_revenue or 0.0,
        "transactions_count": sales.transactions_count or 0
    }

def get_profit_report(db: Session):
    # Calculate profit by joining Sale with Inventory
    sales = db.query(models.Sale, models.Inventory).join(models.Inventory, models.Sale.inventory_id == models.Inventory.id).all()
    total_revenue = sum(sale.Sale.total_price for sale in sales)
    total_cost = sum(sale.Inventory.buying_price * sale.Sale.quantity for sale in sales)
    
    return {
        "total_revenue": total_revenue,
        "total_cost": total_cost,
        "profit": total_revenue - total_cost
    }

