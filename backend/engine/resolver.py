import json
from sqlalchemy.orm import Session
from db.models import Inventory

def resolve_inventory_item(db: Session, spoken_name: str) -> Inventory | None:
    \"\"\"
    Advanced Inventory Resolver.
    Attempts to match the spoken name with the DB using exact match,
    then case-insensitive match, and finally by checking aliases.
    \"\"\"
    spoken_name_lower = spoken_name.lower().strip()
    
    # 1. Try exact match (case insensitive)
    items = db.query(Inventory).all()
    
    for item in items:
        if item.name.lower().strip() == spoken_name_lower:
            return item
            
    # 2. Try aliases
    for item in items:
        try:
            aliases = json.loads(item.aliases)
            if isinstance(aliases, list):
                lower_aliases = [a.lower().strip() for a in aliases]
                if spoken_name_lower in lower_aliases:
                    return item
        except json.JSONDecodeError:
            continue
            
    # 3. Basic fallback (substring match)
    for item in items:
        if spoken_name_lower in item.name.lower().strip():
            return item
            
    return None
