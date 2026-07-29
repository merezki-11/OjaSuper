import json
from sqlalchemy.orm import Session
from db.models import Inventory

def resolve_inventory_item(db: Session, spoken_name: str) -> tuple[Inventory | None, str]:
    """
    Advanced Inventory Resolver.
    Returns (ResolvedItem, error_message_or_follow_up)
    """
    spoken_name_lower = spoken_name.lower().strip()
    
    # 1. Try exact match (case insensitive)
    items = db.query(Inventory).all()
    
    for item in items:
        if item.name.lower().strip() == spoken_name_lower:
            return item, ""
            
    # 2. Try aliases/synonyms
    for item in items:
        try:
            aliases = json.loads(item.aliases)
            if isinstance(aliases, list):
                lower_aliases = [a.lower().strip() for a in aliases]
                if spoken_name_lower in lower_aliases:
                    return item, ""
        except json.JSONDecodeError:
            continue
            
    # 3. Basic fallback (substring match)
    matches = []
    for item in items:
        if spoken_name_lower in item.name.lower().strip():
            matches.append(item)
            
    if len(matches) == 1:
        return matches[0], ""
    elif len(matches) > 1:
        match_names = ", ".join([m.name for m in matches])
        return None, f"Did you mean {match_names}?"
        
    return None, f"Could not find any item matching '{spoken_name}'."
