from Utils.cli_helper import display_header, CYAN, RESET, order_menu


def run_order_menu(order_svc, menu_svc):
    while True:
        display_header("MANAGE ORDERS & BILLING")
        order_menu()
        sub_choice = input(f"\n{CYAN}Choose an option (1-6): {RESET}").strip()

        match sub_choice:
            case "1":
                display_header("CREATE NEW ORDER")

                # 1. Check if the menu has items first
                available_items = menu_svc.get_all_items()
                if not available_items:
                    print("⚠️ The menu is currently empty! Please add items to the menu first.")
                else:
                    # 2. Display available menu items for reference
                    print(f"\n{CYAN}{'Item ID':<10} | {'Name':<20} | {'Price':<8}{RESET}")
                    print("-" * 45)
                    for m_item in available_items:
                        print(f"{m_item.item_id:<10} | {m_item.name:<20} | ${m_item.price:<7.2f}")
                    print("-" * 45 + "\n")

                    order_id = input("Enter Order ID: ").strip()
                    table_id = input("Enter Table ID: ").strip()

                    if not order_id or not table_id:
                        print("❌ Order ID and Table ID cannot be empty!")
                    else:
                        items_list = []
                        while True:
                            item_id_input = input(f"Enter Item ID to order (or type {CYAN}'done'{RESET} to finish): ").strip()
                            if item_id_input.lower() == 'done':
                                break

                            # Look up item from MenuService
                            menu_item = menu_svc.get_item(item_id_input)

                            if menu_item:
                                try:
                                    quantity = int(input(f"Enter quantity for '{menu_item.name}': ").strip())
                                    if quantity <= 0:
                                        print("❌ Quantity must be at least 1!")
                                        continue

                                    items_list.append({
                                        "item_id": menu_item.item_id,
                                        "quantity": quantity,
                                        "price": menu_item.price
                                    })
                                    print(f"✅ Added {quantity}x {menu_item.name} (${menu_item.price:.2f} each)")
                                except ValueError:
                                    print("❌ Invalid input! Quantity must be a whole number.")
                            else:
                                print("❌ Item ID not found on the menu! Please pick a valid ID from above.")

                        # Save order if items were added
                        if items_list:
                            success = order_svc.create_order(order_id, table_id, items_list)
                            if success:
                                print("✅ Order created and saved successfully!")
                        else:
                            print("⚠️ Order creation cancelled (no items added).")

            case "2":
                if not order_svc.get_all_orders():
                    print("\n⚠️ No orders have been placed in the system yet!")
                else:
                    table_id = input("Enter Table ID to view orders: ").strip()
                    if not table_id:
                        print("❌ Table ID cannot be empty!")
                    else:
                        orders = order_svc.get_orders_by_table(table_id)
                        if orders:
                            for ord_obj in orders:
                                print(f"Order ID: {ord_obj.order_id} | Table: {ord_obj.table_id} | Total: ${ord_obj.total_price:.2f}")

            case "3":
                if not order_svc.get_all_orders():
                    print("\n⚠️ No orders have been placed in the system yet!")
                else:
                    table_id = input("Enter Table ID to print receipt: ").strip()
                    if not table_id:
                        print("❌ Table ID cannot be empty!")
                    else:
                        order_svc.generate_receipt(table_id)

            case "4":
                all_orders = order_svc.get_all_orders()
                if all_orders:
                    display_header("ALL SYSTEM ORDERS")
                    print(f"{CYAN}{'Order ID':<12} | {'Table ID':<10} | {'Total Price':<10}{RESET}")
                    print("-" * 40)
                    for ord_obj in all_orders:
                        print(f"{ord_obj.order_id:<12} | {ord_obj.table_id:<10} | ${ord_obj.total_price:<9.2f}")
                    print("-" * 40)
                else:
                    print("⚠️ No orders found in the System!")

            case "5":
                display_header("UPDATE ORDER STATUS")
                order_id = input("Enter Order ID to update: ").strip()

                if not order_id:
                    print("❌ Order ID cannot be empty!")
                else:
                    print("\nSelect new status:")
                    print("1. ⏳ Preparing")
                    print("2. 🔔 Ready")
                    print("3. 🍽️ Served")
                    print("4. ✅ Completed")

                    status_choice = input(f"\n{CYAN}Choose status (1-4): {RESET}").strip()

                    status_map = {
                        "1": "Preparing",
                        "2": "Ready",
                        "3": "Served",
                        "4": "Completed"
                    }

                    if status_choice in status_map:
                        new_status = status_map[status_choice]
                        success = order_svc.update_order_status(order_id, new_status)

                        if success:
                            print(f"✅ Order '{order_id}' status updated to '{new_status}'!")
                        else:
                            print("❌ Order ID not found!")
                    else:
                        print("❌ Invalid status selection.")

            case "6":
                print("Returning to main menu...")
                return  # Directly return to main dashboard without extra pause prompt

            case _:
                print("❌ Invalid selection.")

        input(f"\n{CYAN}Press Enter to continue...{RESET}")