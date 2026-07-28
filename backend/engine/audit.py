import json
from sqlalchemy.orm import Session
from db.models import AuditLog

def log_action(db: Session, action: str, intent_data: dict, is_override: bool = False):
    \"\"\"
    Comprehensive Audit Engine.
    Logs every action, correction, and override.
    \"\"\"
    audit = AuditLog(
        action=action,
        intent_json=json.dumps(intent_data),
        is_override=1 if is_override else 0
    )
    db.add(audit)
    db.commit()
    db.refresh(audit)
    return audit
