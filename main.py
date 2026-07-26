from Utils.cli_helper import display_menu, display_header, CYAN, RESET, display_auth_menu
from Services import auth_service, menu_service, order_service, table_service
import os
import subprocess

menu_svc = menu_service.MenuService()
table_svc = table_service.TableService()
order_svc = order_service.OrderService(menu_svc, table_svc)
auth_svc = auth_service.AuthService()



def login_screen():
    while True:

        subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)

        display_auth_menu()  

        choice = input(f"\n{CYAN}👉 Select an option (1-3): {RESET}").strip()

        match choice:
            case "1":
                display_header("USER LOGIN")
                username = input("Username: ").strip()
                password = input("Password: ").strip()
                if auth_svc.login_user(username, password):
                    print("\n✅ Login successful!")
                    input(f"{CYAN}Press Enter to go to the main menu...{RESET}")
                    return True
                else:
                    # 💡 Pause here so you can read the invalid username/password error!
                    print("\n❌ Login failed! Incorrect username or password.")
                    input(f"{CYAN}Press Enter to try again...{RESET}")
                
            case "2":
                display_header("REGISTER USER")
                user_id = input("Enter User ID: ").strip()
                username = input("Enter Username: ").strip()
                password = input("Enter Password: ").strip()
                role = input("Enter Role (admin/staff) [default: staff]: ").strip().lower() or "staff"
                if auth_svc.register_user(user_id, username, password, role):
                    print("\n✅ User registered successfully! You can now log in.")
                else:
                    print("\n❌ Registration failed! User ID or Username might already exist.")
                
                input(f"\n{CYAN}Press Enter to return to login menu...{RESET}")
                
            case "3":
                print("Goodbye!")
                return False
            
            case _:
                print("❌ Invalid option! Please select 1, 2, or 3.")


def main():
    while True:
        if not login_screen():
           break
     

        logged_in = True
        while logged_in:
            display_menu()

        # Get user selection with styled input prompt
            choice = input(f"\n{CYAN}👉 Select an option (1-6): {RESET}").strip()
            
            match choice:
                case "1" :

                    display_header("ADD NEW TABLE")
                    table_id = input("Enter Table ID:").strip()

                    try :
                        capacity = int(input("Enter the ammount of seats:").strip())
                        table_svc.add_table(table_id, capacity)
                    except ValueError :
                        print("❌ Invalid input! Capacity must be a number.")
                
                case "2":
                    display_header("FIND TABLE DETAILS")
                    table_id = input("Enter table ID: ").strip()
                    table = table_svc.find_table(table_id)
            
                    if table:
                        print(table.get_details())

                case "3" :

                    display_header("SHOW AVAILABLE TABLE")
                    try :
                        party_size = int(input("Enter the ammount of people :").strip())
                        available_tables = table_svc.get_available_tables(party_size)
                        
                        if available_tables :
                            for a in available_tables :
                                print(f"Table ID: {a.table_id} | Capacity: {a.capacity}")
                        else :
                            print("No available tables found for that party size.")

                    except ValueError :
                        print("❌ Invalid input! ammount of people must be a number.")
                    
                    
                case "4" :

                    display_header("OCCUPY A TABLE")
                    table_id = input("Enter Table ID: ").strip()

                    try :
                        party_size = int(input("Enter the ammount of people: ").strip())
                        table_svc.occupy_table(table_id, party_size)
                    except ValueError :
                        print("❌ Invalid input! ammount of people must be a number.")

                case "5" :

                    display_header("VACATE A TABLE")
                    table_id = input("Enter Table ID: ").strip()
                    table_svc.vacate_table(table_id)
                
                case "6" :
                    auth_svc.logout()
                    logged_in = False
                    break

                case _:
                    print("❌ Invalid choice! Please select a valid option from the menu.")

if __name__ == "__main__":
   main()
