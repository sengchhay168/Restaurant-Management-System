# Color Shortcuts
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

def display_header(title):
    # Centered header box
    border = "═" * (len(title) + 4)
    print(f"\n\t\t{CYAN}╔{border}╗")
    print(f"\t\t║  {title}  ║")
    print(f"\t\t╚{border}╝{RESET}")

def display_menu():
    # Perfectly aligned dashboard box with uniform tab spacing
    print(f"\n\t{CYAN}┌──────────────────────────────────────────┐")
    print(f"\t│       ✨ RESTAURANT DASHBOARD ✨         │")
    print(f"\t├──────────────────────────────────────────┤{RESET}")
    print(f"\t│   [{GREEN}1{RESET}]  ➕  Add New Table                 │")
    print(f"\t│   [{GREEN}2{RESET}]  🔍  Find Table Details            │")
    print(f"\t│   [{GREEN}3{RESET}]  📋  Show Available Tables         │")
    print(f"\t│   [{YELLOW}4{RESET}]  🪑  Occupy a Table                │")
    print(f"\t│   [{YELLOW}5{RESET}]  🧹  Vacate a Table                │")
    print(f"\t│   [{CYAN}6{RESET}]  🍔  Manage Orders & Billing       │")
    print(f"\t│   [{CYAN}7{RESET}]  📜  Manage Restaurant Menu        │")
    print(f"\t│   [{RED}8{RESET}]  ❌  Exit System                   │")
    print(f"\t{CYAN}└──────────────────────────────────────────┘{RESET}")


def display_auth_menu():
    """Displays a styled box menu for login and registration."""
    print(f"\n{CYAN}┌───────────────────────────────────────┐{RESET}")
    print(f"{CYAN}│        🔐 WELCOME TO RESTAURANT       │{RESET}")
    print(f"{CYAN}├───────────────────────────────────────┤{RESET}")
    print(f"{CYAN}│  [1] 🔑 Login                         │{RESET}")
    print(f"{CYAN}│  [2] 👤 Register New User             │{RESET}")
    print(f"{CYAN}│  [3] ❌ Exit Application              │{RESET}")
    print(f"{CYAN}└───────────────────────────────────────┘{RESET}")

def order_menu():
    print(f"\n\t{CYAN}┌──────────────────────────────────────────┐")
    print(f"\t│      🍔 MANAGE ORDERS & BILLING          │")
    print(f"\t├──────────────────────────────────────────┤{RESET}")
    print(f"\t│   [{GREEN}1{RESET}]  ➕  Create New Order              │")
    print(f"\t│   [{GREEN}2{RESET}]  🔍  View Orders by Table          │")
    print(f"\t│   [{GREEN}3{RESET}]  🧾  Generate Receipt & Pay        │")
    print(f"\t│   [{CYAN}4{RESET}]  📋  View All System Orders        │")
    print(f"\t│   [{YELLOW}5{RESET}]  🔄  Update Order Status           │") 
    print(f"\t│   [{RED}6{RESET}]  ↩️   Exit / Back to Main Menu      │")  
    print(f"\t{CYAN}└──────────────────────────────────────────┘{RESET}")

def menu_dashboard_ui():
    print(f"\n\t{CYAN}┌──────────────────────────────────────────┐")
    print(f"\t│       📜 MANAGE RESTAURANT MENU          │")
    print(f"\t├──────────────────────────────────────────┤{RESET}")
    print(f"\t│   [{GREEN}1{RESET}]  📋  View All Menu Items           │")
    print(f"\t│   [{GREEN}2{RESET}]  ➕  Add New Menu Item             │")
    print(f"\t│   [{GREEN}3{RESET}]  🔍  Search Menu Items             │")
    print(f"\t│   [{CYAN}4{RESET}]  🗑️   Delete Menu Item              │")
    print(f"\t│   [{RED}5{RESET}]  ↩️   Exit / Back to Main Menu      │")
    print(f"\t{CYAN}└──────────────────────────────────────────┘{RESET}")


