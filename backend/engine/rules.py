from sqlalchemy.orm import Session
from db.models import Inventory, Customer
from datetime import datetime

def execute_business_rules(db: Session, intent_data: dict) -> tuple[bool, str, list]:
    \"\"\"
    Business Rules Engine: Checks DB state before execution.
    Returns (is_allowed: bool, blocker_error: str, warnings: list)
    \"\"\"
    warnings = []
    intent = intent_data.get("intent")
    
    if intent == "Record Sale":
        for item in intent_data.get("items", []):
            db_item = db.query(Inventory).filter(Inventory.name == item.get("name")).first()
            
            # Blocker: Unknown product (if resolver failed to normalize)
            if not db_item:
                return False, f"Item {item.get('name')} not found in inventory.", warnings
                
            # Blocker: Negative Stock Prevention
            if db_item.quantity < item.get("quantity"):
                return False, f"Insufficient stock for {item.get('name')}. Available: {db_item.quantity}", warnings
                
            # Warning: Selling below buying price (Profit check)
            if db_item.selling_price < db_item.buying_price:
                warnings.append(f"Warning: Selling {db_item.name} at a loss.")
                
            # Warning: Expiry check
            if db_item.expiry_date and db_item.expiry_date < datetime.now():
                warnings.append(f"Warning: {db_item.name} is past its expiry date.")
                
    elif intent == "Modify Item" or intent == "Create Item":
        # Blocker: Duplicate name check
        new_name = intent_data.get("name")
        if new_name:
            existing = db.query(Inventory).filter(Inventory.name == new_name).first()
            # If creating or modifying to an already existing name
            if existing and intent_data.get("id") != existing.id:
                return False, f"Item with name '{new_name}' already exists.", warnings
                
    elif intent == "Create Customer":
        # Blocker: Duplicate phone number
        phone = intent_data.get("phone_number")
        if phone:
            existing = db.query(Customer).filter(Customer.phone_number == phone).first()
            if existing:
                return False, f"Customer with phone {phone} already exists.", warnings

    return True, "Execution rules passed.", warnings
