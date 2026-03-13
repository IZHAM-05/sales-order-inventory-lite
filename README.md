# Vikmo - Sales Order & Inventory Lite

A B2B SaaS backend for auto parts distribution. This system handles dealer management, product catalogs, real-time inventory tracking, and a full sales order lifecycle.

## 🚀 Key Features & Business Rules

### 1. Advanced Inventory Control
- **Stock Validation**: Orders are strictly validated against available stock. Attempting to confirm an order with insufficient stock results in a descriptive error: *"Insufficient stock for [Product]. Available: X, Requested: Y"*.
- **Stock Deduction**: Inventory is only deducted when an order transitions from `Draft` → `Confirmed`.
- **Race Condition Protection**: Uses `transaction.atomic()` and `select_for_update()` to ensure data integrity during high-concurrency order confirmations.

### 2. Order Lifecycle Management
- **Status Flow**: Enforces the strict progression: `Draft` → `Confirmed` → `Delivered`.
- **Immutable Orders**: Once an order is `Confirmed` or `Delivered`, it is locked and cannot be modified, ensuring financial auditability.
- **Price Preservation**: Captures the `unit_price` at the moment of order creation. Future price changes in the product catalog do not retroactively affect existing orders.

### 3. Automated Logic
- **Order Numbering**: Auto-generates unique IDs following the format: `ORD-YYYYMMDD-XXXX`.
- **Calculations**: Automatically computes `line_total` (Quantity × Price) and `total_amount` for the entire order.

---

## 🛠️ Technical Stack
- **Backend**: Python 3.12.9 + Django 6.0.3 + Django REST Framework
- **Database**: SQLite (Configured for easy review/setup)
- **API Design**: RESTful JSON APIs

---

## ⚙️ Project Setup

### 1. Installation
```bash
git clone https://github.com
cd sales-order-inventory-lite
python -m venv venv

# On Windows:
.\venv\Scripts\activate

pip install -r requirements.txt
python manage.py migrate
Use code with caution.

2. Running the Project
bash
python manage.py runserver
Use code with caution.

Access API at: 127.0.0.1
📝 API Endpoints
Method	Endpoint	Description
GET	/api/products/	List all products with current stock levels
POST	/api/dealers/	Register a new B2B dealer
POST	/api/orders/	Create a new Draft order
POST	/api/orders/{id}/confirm/	Validate stock & move to Confirmed
POST	/api/orders/{id}/deliver/	Finalize order status to Delivered
PUT	/api/inventory/{product_id}/	Manual stock adjustment (Admin only)
🧪 Test Scenarios Handled
Scenario A (Success): Create product (100 stock) → Create draft order (10 units) → Confirm → Stock drops to 90.
Scenario B (Failure): Product has 5 units → Order requests 10 → Attempt to confirm → Returns 400 Error with stock details.
Scenario C (Validation): Attempting to move an order from Delivered back to Draft is rejected.
📂 Database Schema Design
Product: Catalog with unique SKU and current pricing.
Inventory: 1:1 relationship with Product tracking quantity.
Dealer: Customer information and unique identification.
Order: Main tracking record with auto-numbering and total amount.
OrderItem: Line items linking orders to products with "frozen" unit prices.
Author: Izham | Vikmo Fresher Assignment - March 2026
