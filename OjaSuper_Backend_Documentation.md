# OjaSuper Backend Architecture & API Summary

**Author:** Backend Development Team  
**Prepared For:** Eddie & Prince (Frontend Team)

This document provides a high-level summary of the OjaSuper Backend architecture, database schema, and API routes. It is designed to get you up to speed quickly so you can start connecting the frontend.

---

## 1. Tech Stack Overview
- **Framework:** FastAPI (Python)
- **Database:** SQLite (using SQLAlchemy ORM)
- **Data Validation:** Pydantic
- **AI Integration:** Mocked LLM intent extraction and Speech-to-Text (ready to be swapped with Phi-3 / Whisper later)

---

## 2. Core Concepts & Workflow

The most critical endpoint is `/voice`. Here is the lifecycle of a voice command:
1. **Audio Upload:** Frontend sends an audio file to `/voice`.
2. **STT (Speech-to-Text):** Converts audio to text (currently mocked in `ai/stt.py`).
3. **Intent Extraction:** The LLM categorizes the text into structured JSON intents (e.g., `Record Sale`, `Restock`, `Inventory Query`).
4. **Validation Layer:** `engine/validation.py` checks for required fields, valid dates, and positive quantities.
5. **Resolver:** `engine/resolver.py` maps spoken product names to actual database IDs using exact matches, aliases/synonyms, and substring matching. If it finds multiple matches, it returns a follow-up question (e.g., "Did you mean 50kg rice or 10kg rice?").
6. **Business Rules Engine:** `engine/rules.py` enforces strict business logic (e.g., blocking sales if stock is negative, requiring manager approval for massive sales, warning if an item is sold below cost price).
7. **Execution:** If all checks pass, `crud.py` executes the database transaction.

---

## 3. Database Models (`db/models.py`)

The database is built using SQLAlchemy. The core tables are:
- **`Inventory`**: Tracks items (`id`, `name`, `quantity`, `buying_price`, `selling_price`, `expiry_date`, `aliases`).
- **`Sale`**: Tracks item sales (`inventory_id`, `quantity`, `total_price`, `discount`, `is_refund`, `is_return`, `override_reason`).
- **`Purchase`**: Tracks restocking history.
- **`Customer`**: Tracks customer details (`name`, `phone_number`, `credit_balance`).
- **`Transaction`**: Tracks a customer's credit and payments (Ledger).
- **`Employee`**: Tracks staff for authentication (`username`, `role` - either cashier or manager).
- **`Setting`**: Key-value pair configurations for the store.
- **`AuditLog`**: Tracks every action and AI command executed on the system for security purposes.

---

## 4. API Endpoints (`api/routes.py`)

All endpoints are built out and ready to consume. They follow standard RESTful patterns and return JSON defined in `api/schemas.py`.

### 🎙️ AI Engine
- `POST /voice`: Accepts an audio file upload and processes the entire AI pipeline.

### 📦 Inventory
- `GET /inventory/`: List all items.
- `POST /inventory/`: Create a new item.
- `PUT /inventory/{id}`: Update an item.
- `DELETE /inventory/{id}`: Delete an item.

### 💰 Sales & Restocking
- `GET /sales/` & `POST /sales/`: Manage sales records.
- `GET /purchases/` & `POST /purchases/`: Manage restocking records.

### 👥 Customers & Credit
- `GET /customers/` & `POST /customers/`: Manage customers.
- `GET /transactions/` & `POST /transactions/`: Manage customer credit ledger (payments vs debts).

### 📊 Reports
- `GET /reports/daily`: Returns today's total revenue and transaction count.
- `GET /reports/profit`: Computes overall cost of goods sold vs revenue for net profit.

### ⚙️ System
- `POST /employees/`: Register new employees.
- `GET /settings/{key}` & `POST /settings/`: Manage store configurations.

---

## 5. Where to Start Reading the Code?

If you are diving into the codebase today, I recommend reading the files in this specific order:
1. **`db/models.py`** -> Understand how the database is structured.
2. **`api/schemas.py`** -> See the exact JSON structures the frontend needs to send and receive.
3. **`api/routes.py`** -> Look at the API endpoints available for the frontend to hit.
4. **`engine/rules.py`** -> Understand what rules might block a request (so you can handle those 400 Errors on the frontend).
