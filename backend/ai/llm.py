import json
from .prompts import INTENT_SYSTEM_PROMPT

def extract_intent_mock(text: str) -> dict:
    \"\"\"
    Mocks the LLM intent extraction.
    In the real implementation, this will use llama-cpp-python and Phi-3.
    \"\"\"
    text_lower = text.lower()
    
    if "sold" in text_lower or "sell" in text_lower:
        return {
            "intent": "Record Sale",
            "items": [{"name": "rice", "quantity": 5}],
            "total_price": 15000,
            "confidence": 0.95
        }
    elif "bought" in text_lower or "restock" in text_lower:
        return {
            "intent": "Restock",
            "items": [{"name": "rice", "quantity": 50, "cost_price": 25000}],
            "confidence": 0.92
        }
    elif "profit" in text_lower:
        return {"intent": "Profit Query", "confidence": 0.9}
    elif "credit" in text_lower or "owe" in text_lower:
        return {"intent": "Credit Query", "customer": "john", "confidence": 0.85}
        
    return {"intent": "Unknown", "confidence": 0.1}
