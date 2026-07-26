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

## ✨ Features
- **Authentication System**: Secure user registration and login with role-based options (admin / staff).
- **Data Persistence**: Automatic saving and loading of system data via JSON files.
- **Table Management**: View table availability and handle table assignments.
- **Menu & Order Handling**: Manage menu items and customer order workflows.

---

## 📁 Project Structure

```text
RESTAURANT SYSTEM/
│
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
```
