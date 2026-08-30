# 🍽️ Restaurant Management System

A full-stack Streamlit web application designed for managing restaurant operations, featuring user authentication, interactive POS ordering, table tracking, menu management, and automated billing. Built with object-oriented programming (OOP) principles and a modular architecture.

---

## 🚀 How to Run

1. Open a terminal in the project root directory (`RESTAURANT SYSTEM`).
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## ✨ Features
- **Modern Dark Theme UI**         : Designed with a sleek, high-end POS dark aesthetic and a real-time live ticking clock in the sidebar.
- **User Authentication**          : Secure multi-role support (admin and staff) with a centered login portal and toggleable user registration.
- **Point of Sale (POS)**          : Interactive cart and order builder mapped directly to active restaurant tables.
- **Table Management**             : Track table capacities, toggle occupancy states, and automatically vacate tables upon checkout completion.
- **Menu Management**              : Dynamic backend integration to view, add, and delete menu items stored via JSON.
- **Automated Billing & Checkout** : Cleanly formatted pandas-based receipt printouts supporting custom discount percentages, tax calculation, and a one-click "Finished Paying" feature that clears orders and frees up tables.
---

## 📁 Project Structure

```text
RESTAURANT SYSTEM/
│
├── .streamlit/             # Streamlit configuration settings
│   └── config.toml
├── Data/                   # Stored JSON database files
│   ├── menu.json
│   ├── orders.json
│   ├── tables.json
│   └── users.json
│
├── Models/                 # Data classes (User, Table, MenuItem, Order)
├── Services/               # Core business logic (Auth, Table, Menu, Order services)
├── Utils/                  # Helper scripts and formatting tools
├── app.py                  # Main Streamlit web application entry point
├── main.py                 # CLI entry point (legacy support)
├── README.md               # Project documentation
└── requirements.txt        # Project dependencies (streamlit, pandas, etc.)