# SALES ORDER & INVENTORY LITE API

This project is a robust backend system built using **Django** and **Django REST Framework**. It is designed to manage the lifecycle of B2B sales orders for auto parts distribution, including **dealers, products, inventory, and automated order workflows**.

The system ensures data integrity by validating stock availability before confirmation and preserving historical pricing at the time of purchase.

---

# 🚀 KEY FEATURES

**• Dealer Management**: Full API support for managing B2B dealer profiles.

**• Product & Inventory**: Real-time tracking of stock levels with 1:1 product mapping.

**• Atomic Stock Validation**: Prevents over-selling by checking inventory levels during order confirmation.

**• Race Condition Protection**: Uses database-level locking (select_for_update) to ensure stock integrity.

**• Price Preservation**: Automatically locks the unit_price at the moment of order to protect against future price changes.

**• Automatic Order Numbering**: Generates unique IDs in the format ORD-YYYYMMDD-XXXX.

---

# 🛠️ TECH STACK

**• Language**: Python 3.12.9

**• Framework**: Django 6.0.3 & Django REST Framework

**• Database**: SQLite (Configured for easy review/setup)

---

# 📂 PROJECT STRUCTURE

**• dealers/** - Dealer profiles and management APIs

**• products/** - Product catalog and pricing

**• inventory/** - Real-time stock tracking and adjustments

**• orders/** - Order creation, validation, and lifecycle workflows

---

# ⚙️ HOW TO RUN THE PROJECT

**1. Clone the Repository**
`git clone https://github.com/IZHAM-05/sales-order-inventory-lite`

**2. Navigate to the Project Folder**
`cd sales-order-inventory-lite`

**3. Create Virtual Environment**
`python -m venv venv`

**4. Activate Virtual Environment**
- **Windows**: `.\venv\Scripts\activate`
- **Mac / Linux**: `source venv/bin/activate`

**5. Install Dependencies**
`pip install -r requirements.txt`

**6. Run Database Migrations**
`python manage.py makemigrations`
`python manage.py migrate`

**7. Run the Development Server**
`python manage.py runserver`

*Server will start at: http://127.0.0.1*

---

# 📝 API ENDPOINTS

**• /api/dealers/** : Manage B2B Dealer records

**• /api/products/** : Manage Product catalog

**• /api/inventory/** : Track and adjust stock levels

**• /api/orders/** : Create and list Sales Orders

**• /api/orders/{id}/confirm/** : POST to validate stock and deduct inventory

**• /api/orders/{id}/deliver/** : POST to mark an order as completed

---

# 🔄 ORDER WORKFLOW

Orders follow a strict lifecycle to ensure business reliability:

**Draft → Confirmed → Delivered**

**• Draft**: Orders are created here. This is the only stage where items can be edited.

**• Confirmed**: Triggered by the /confirm/ action. Stock is checked and deducted atomically.

**• Delivered**: Final stage marking the successful completion of the order.

**Rules**:
- Confirmation fails if stock is insufficient.
- Once Confirmed, the order is locked and cannot be modified.

---

# 🧪 API TESTING (cURL EXAMPLES)

You can test the order actions using these terminal commands:

**1. Confirm Order (Deduct Stock)**
`curl -X POST http://127.0.0.1api/orders/1/confirm/`

**2. Deliver Order**
`curl -X POST http://127.0.0.1api/orders/1/deliver/`

**3. Place Order (Directly)**
`curl -X POST http://127.0.0.1api/orders/place_order/ -H "Content-Type: application/json" -d "{\"dealer\": 1, \"product\": 1, \"quantity\": 5}"`

---



# 👤 AUTHOR

**Izham**
*Backend Developer Assignment - March 2026*