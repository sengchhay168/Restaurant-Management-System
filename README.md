# 🍽️ Restaurant Management System

A Python CLI application designed for managing restaurant seating, user authentication, menu items, and customer orders. Built with OOP (Object-Oriented Programming) principles and modular architecture.

---

## 🚀 How to Run

1. Open a terminal in the project root directory (`RESTAURANT SYSTEM`).
2. Run the application:
   ```bash
   python main.py
```

---

## Features
- **User Authentication:** Multi-role support (`admin` and `staff`).
- **Access Control:** Restricted menu management for non-admin users.
- **Table & Order Management:** Assign tables, create orders, track statuses.
- **Receipt & Billing:** Automated calculation of subtotal, customizable discount %, and tax.
---

## 📁 Project Structure

```text
RESTAURANT SYSTEM/
│
├── Controller/           # CLI controllers & user flow logic (menu, order)
├── Data/                 # Stored JSON files (users, tables, menu, orders)
│   ├── menu.json
│   ├── orders.json
│   ├── tables.json
│   └── users.json
│
├── Models/               # Data classes (User, Table, MenuItem, Order)
├── Services/             # Core business logic (Auth, Table, Menu, Order services)
├── Utils/                # Helper scripts (CLI formatting, File handling)
├── main.py               # Main application entry point
├── README.md             # Project documentation
└── requirements.txt      # Project dependencies