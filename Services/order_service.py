from Models import order
from Utils import file_handler

orders_cls = order.Order
file = file_handler.FileHandler()

class OrderService:
    def __init__(self, menu_service, table_service, data_file="Data/orders.json"):
        self.menu_service = menu_service
        self.table_service = table_service
        self.data_file = data_file
        self.orders = self._load_orders()

    def _load_orders(self):
        """Loads data from JSON and converts them into Order objects."""
        raw_data = file.read_json(self.data_file, [])
        converted_item = []

        for order_dict in raw_data:
            order_obj = orders_cls.from_dict(order_dict) 
            converted_item.append(order_obj) 
        return converted_item
      
    def _save_orders(self):
        dict_list = []

        for order_item in self.orders:
            order_as_dictionary = order_item.to_dict() 
            dict_list.append(order_as_dictionary)
            
        file.write_json(self.data_file, dict_list)

    def create_order(self, order_id, table_id, items) :
        for o in self.orders :
            if order_id == o.order_id :
                print("❌ Order ID already exists!")
                return False
            
        total_price = 0.0

        for item in items:
            quantity = item["quantity"]
            
            # Check if a custom price was passed, otherwise look it up or use a default $5.00 price
            if "price" in item:
                item_price = item["price"]
            else:
                item_id = item["item_id"]
                menu_item = self.menu_service.get_item(item_id) if hasattr(self.menu_service, 'get_item') else None
                item_price = menu_item.price if menu_item else 5.00
            
            total_price += item_price * quantity
            
        new_order = orders_cls(order_id, table_id, items, total_price=total_price)
        self.orders.append(new_order)
        self._save_orders()  
        return True

    
    def get_orders_by_table(self, table_id):
            """Returns all orders for a specific table."""
            # Ensure self.orders is up to date (if you have a reload method, call it here)
            if hasattr(self, 'load_orders'):
                self.load_orders()

            matching_orders = []
            for o in self.orders:
                # Check if 'o' is a dictionary or an Order object
                current_table = o.get("table_id") if isinstance(o, dict) else getattr(o, "table_id", None)
                
                if current_table and str(current_table).strip().lower() == str(table_id).strip().lower():
                    matching_orders.append(o)
                    
            return matching_orders
                    
    def get_all_orders(self):
        if not self.orders :
            print("⚠️ No orders have been placed yet!")
            return []
        else:
            return self.orders
        

    def generate_receipt(self, table_id, discount_percent=0.0):
        """Prints a formatted receipt for all orders at a specific table."""
        # 1. Get all orders for this table
        orders = self.get_orders_by_table(table_id)
        
        # 2. If no orders found, exit early
        if not orders:
            print(f"\n[!] No active orders found for Table {table_id}.")
            input("\nPress Enter to return to main menu...")
            return

        # 3. Print receipt header
        print("=" * 40)
        print(f"RECEIPT: TABLE {table_id}".center(40))
        print("=" * 40)
        print(f"{'Item':<20}{'Qty':<5}{'Price':<7}{'Subtotal':<8}")
        print("-" * 40)

        raw_subtotal = 0.0

        # 4. Loop through every order and every item
        for order in orders:
            for item in order.items:
                quantity = item["quantity"]
                item_id = item["item_id"]
                
                # Check menu service first, or fall back to saved price
                menu_item = self.menu_service.get_item(item_id)
                
                if menu_item:
                    name = menu_item.name
                    price = menu_item.price
                else:
                    name = item_id
                    price = item.get("price", 5.00)

                # These 3 lines are placed OUTSIDE the else block so EVERY item prints!
                item_subtotal = price * quantity
                raw_subtotal += item_subtotal
                print(f"{name:<20}{quantity:<5}${price:<6.2f}${item_subtotal:<7.2f}")

        # 5. Calculate totals OUTSIDE the loops using raw_subtotal
        discount_amount = raw_subtotal * (discount_percent / 100)
        taxable_amount = raw_subtotal - discount_amount
        tax = taxable_amount * 0.05
        grand_total = taxable_amount + tax
        
        # 6. Print receipt footer
        print("-" * 40)
        print(f"{'Subtotal:':<30}${raw_subtotal:>7.2f}")
        if discount_percent > 0:
            print(f"{f'Discount ({discount_percent}%):':<30}-${discount_amount:>7.2f}")
        print(f"{'Tax (5%):':<30}+${tax:>7.2f}")
        print("=" * 40)
        print(f"{'GRAND TOTAL:':<30}${grand_total:>7.2f}")
        print("=" * 40)
        
    def update_order_status(self, order_id, new_status):
            """Updates the status of an existing order and saves to JSON."""
            for order in self.orders:
                if order.order_id == order_id:
                    order.status = new_status
                    self._save_orders()  
                    return True
            return False

    def delete_orders_by_table(self, table_id):
        """Deletes all orders associated with a specific table after payment."""
        initial_count = len(self.orders)
        self.orders = [o for o in self.orders if str(o.table_id).strip().lower() != str(table_id).strip().lower()]

        if len(self.orders) < initial_count:
            self._save_orders()
            return True
        return False