from Utils.cli_helper import menu_dashboard_ui, display_header, CYAN, RESET


def run_menu_management(menu_svc):
    while True:
        display_header("Management Restaurant Menu")
        menu_dashboard_ui()
        choice = input(f"\n{CYAN}Choose an option (1-5): {RESET}").strip()

        match choice:
            case "1":
                items = menu_svc.get_all_items()

                if items:
                    print(f"{'Item ID':<10} | {'Name':<20} | {'Category':<15} | {'Price':<8}")
                    print("-" * 60)

                    for item in items:
                        print(f"{item.item_id:<10} | {item.name:<20} | {item.category:<15} | ${item.price:<7.2f}")
                    
                    print("-" * 60)
                else:
                    print("⚠️ The menu is currently empty!")

            case "2":
                display_header("Add New Menu Item")

                item_id = input("Enter Item ID: ").strip()
                if not item_id:
                    print("❌ Item ID cannot be empty!")
                else:
                    name = input("Enter Item Name: ").strip()
                    category = input("Enter Item Category: ").strip()

                    if not name or not category:
                        print("❌ Name and Category cannot be empty!")
                    else:
                        try:
                            price = float(input("Enter Item Price ($): ").strip())
                            if price <= 0:
                                print("❌ Price must be greater than $0.00!")
                            else:
                                success = menu_svc.add_item(item_id, name, category, price)
                                if success:
                                    print(f"✅ Item '{name}' added successfully!")
                                else:
                                    print("❌ Could not add item! Item ID already exists.")
                        except ValueError:
                            print("❌ Invalid price! Price must be a valid number.")

            case "3":
                display_header("Search Menu Items")

                keyword = input("Enter Item name: ").strip()
                results = menu_svc.search_items(keyword)

                if results:
                    print(f"{'Item ID':<10} | {'Name':<20} | {'Category':<15} | {'Price':<8}")
                    print("-" * 60)

                    for item in results:
                        print(f"{item.item_id:<10} | {item.name:<20} | {item.category:<15} | ${item.price:<7.2f}")
                else:
                    print("⚠️ No items found!")

            case "4":
                display_header("Delete Menu Item")

                item_id = input("Enter Item ID: ").strip()
                if not item_id:
                    print("❌ Item ID cannot be empty!")
                else:
                    result = menu_svc.delete_item(item_id)
                    if result:
                        print("✅ Item has been successfully deleted!")
                    else:
                        print("❌ Invalid Item ID!")

            case "5":
                print(f"{CYAN}Returning to Main Menu...{RESET}")
                break

            case _:
                print("❌ Invalid Option!")

        input(f"\n{CYAN}Press Enter to continue...{RESET}")