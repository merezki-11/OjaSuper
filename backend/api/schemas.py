from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# --- INVENTORY SCHEMAS ---
class InventoryBase(BaseModel):
    name: str
    quantity: int = 0
    buying_price: float = 0.0
    selling_price: float
    aliases: str = "[]"

class InventoryCreate(InventoryBase):
    pass

class InventoryUpdate(BaseModel):
    name: Optional[str] = None
    quantity: Optional[int] = None
    buying_price: Optional[float] = None
    selling_price: Optional[float] = None
    aliases: Optional[str] = None

class InventoryResponse(InventoryBase):
    id: int

    class Config:
        from_attributes = True

# --- CUSTOMER SCHEMAS ---
class CustomerBase(BaseModel):
    name: str
    phone_number: Optional[str] = None
    credit_balance: float = 0.0

class CustomerCreate(CustomerBase):
    pass

class CustomerResponse(CustomerBase):
    id: int

    class Config:
        from_attributes = True

# --- SALES SCHEMAS ---
class SaleBase(BaseModel):
    inventory_id: int
    quantity: int
    total_price: float
    customer_id: Optional[int] = None

class SaleCreate(SaleBase):
    pass

class SaleResponse(SaleBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# --- PURCHASE SCHEMAS ---
class PurchaseBase(BaseModel):
    inventory_id: int
    quantity: int
    cost_price: float

class PurchaseCreate(PurchaseBase):
    pass

class PurchaseResponse(PurchaseBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# --- EMPLOYEE SCHEMAS ---
class EmployeeBase(BaseModel):
    username: str
    role: str = "cashier"

class EmployeeCreate(EmployeeBase):
    password: str

class EmployeeResponse(EmployeeBase):
    id: int

    class Config:
        from_attributes = True

# --- SETTING SCHEMAS ---
class SettingBase(BaseModel):
    key: str
    value: str

class SettingCreate(SettingBase):
    pass

class SettingResponse(SettingBase):
    class Config:
        from_attributes = True

# --- TRANSACTION SCHEMAS ---
class TransactionBase(BaseModel):
    customer_id: int
    amount: float
    transaction_type: str

class TransactionCreate(TransactionBase):
    pass

class TransactionResponse(TransactionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

