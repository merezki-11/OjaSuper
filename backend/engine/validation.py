def validate_intent(intent_data: dict) -> tuple[bool, str]:
    \"\"\"
    Validation Layer: Checks for missing fields, invalid quantities, dates, and confidence.
    Returns (is_valid, error_message)
    \"\"\"
    # 1. Confidence Threshold Check (Assuming AI outputs a confidence score)
    confidence = intent_data.get("confidence", 1.0)
    if confidence < 0.7:
        return False, f"AI confidence too low ({confidence}). Please repeat clearly."
        
    intent = intent_data.get("intent")
    
    if not intent or intent == "Unknown":
        return False, "Could not understand the command."
    
    # 2. Intent-specific structural validation
    if intent in ["Record Sale", "Record Purchase", "Restock"]:
        if not intent_data.get("items"):
            return False, f"No items found for {intent}."
        for item in intent_data.get("items", []):
            if item.get("quantity", 0) <= 0:
                return False, f"Invalid quantity for {item.get('name')}"
            if intent in ["Record Purchase", "Restock"] and item.get("cost_price", 0) <= 0:
                return False, f"Invalid cost price for {item.get('name')}"
                
    elif intent == "Modify Item":
        if not intent_data.get("name"):
            return False, "Item name is required for modification."
            
    # 3. Date Validation (if applicable)
    date_str = intent_data.get("date")
    if date_str:
        from datetime import datetime
        try:
            datetime.fromisoformat(date_str)
        except ValueError:
            return False, f"Invalid date format provided: {date_str}"
            
    return True, ""
