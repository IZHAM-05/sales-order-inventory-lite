# Sales Order & Inventory Lite API

This project is built using **Django** and **Django REST Framework**.  
It provides a simple backend system to manage **dealers, products, inventory, and sales orders**.

The system supports creating orders, confirming them based on stock availability, and delivering them while maintaining proper inventory control.

---

# Features

• Dealer Management API  
• Product Management API  
• Inventory Management  
• Order Creation  
• Order Confirmation with Stock Validation  
• Order Delivery Workflow  
• Automatic Order Number Generation  
• Inventory Update on Order Confirmation  

---

# Tech Stack

• Python  
• Django  
• Django REST Framework  
• SQLite  

---

# Project Structure


dealers/ - Dealer APIs
products/ - Product APIs
inventory/ - Inventory management
orders/ - Order management
manage.py - Django project entry point


---

# How to Run the Project

### 1. Clone the Repository


git clone <your-repository-url>


### 2. Navigate to the Project Folder


cd sales-order-inventory-lite


### 3. Create Virtual Environment


python -m venv venv


### 4. Activate Virtual Environment

Windows


venv\Scripts\activate


Mac / Linux


source venv/bin/activate


### 5. Install Dependencies


pip install -r requirements.txt


### 6. Run Database Migrations


python manage.py makemigrations
python manage.py migrate


### 7. Run the Development Server


python manage.py runserver


Server will start at:


http://127.0.0.1:8000/


---

# API Endpoints

| Endpoint | Description |
|--------|--------|
| /api/dealers/ | Dealer management |
| /api/products/ | Product management |
| /api/inventory/ | Inventory management |
| /api/orders/ | Order management |

---

# Order Workflow

Orders follow this lifecycle:


Draft → Confirmed → Delivered


Rules:

• Orders are created in **Draft** status  
• Only **Draft orders** can be edited  
• Order confirmation checks **inventory availability**  
• If stock is insufficient, confirmation fails  
• Confirmed orders cannot be modified  
• Delivered orders mark completion of the order  

---

# Example Order Flow

1. Create Product  
2. Add Inventory Stock  
3. Create Dealer  
4. Place Order  
5. Confirm Order (stock deducted)  
6. Deliver Order  

---

# Author

Izham
