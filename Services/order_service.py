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

    
    def get_orders_by_table(self, table_id) :
        matching_orders = []
        for o in self.orders :
            if table_id == o.table_id :
                matching_orders.append(o)
            
        if matching_orders: 
            return matching_orders
            
        else:
            print("❌ No orders found for this table ID!")
            return []
            
    def get_all_orders(self):
        if not self.orders :
            print("⚠️ No orders have been placed yet!")
            return []
        else:
            return self.orders
        

    def generate_receipt(self, table_id):
        """Prints a formatted receipt for all orders at a specific table."""
        # 1. Get all orders for this table
        orders = self.get_orders_by_table(table_id)
        
        # 2. If the returned list is empty, exit early
        if not orders:
            print(f"\n[!] No active orders found for Table {table_id}.")
            input("\n{Press Enter to Go back to the main Menu}: ")
            return

        # 3. Print the top header of the receipt
        print("=" * 40)
        print(f"RECEIPT: TABLE {table_id}".center(40))
        print("=" * 40)
        # This line prints the static text headers for the columns
        print(f"{'Item':<20}{'Qty':<5}{'Price':<7}{'Subtotal':<8}")
        print("-" * 40)

        grand_total = 0.0

        # 4. Loop through every item in every order
        for order in orders:
            for item in order.items:
                quantity = item["quantity"]
                
                # Check menu service first, otherwise use custom item_id and fallback price
                item_id = item["item_id"]
                menu_item = self.menu_service.get_item(item_id) if hasattr(self.menu_service, 'get_item') else None
                
                if menu_item:
                    name = menu_item.name
                    price = menu_item.price
                else:
                    name = item_id  # Use the typed name (e.g., "Burger")
                    price = item.get("price", 5.00)  # Use the saved price, or $5.00 default
                
                subtotal = price * quantity
                grand_total += subtotal
                print(f"{name:<20}{quantity:<5}${price:<6.2f}${subtotal:<7.2f}")

        # 5. Print the grand total footer (outside the loops!)
        print("-" * 40)
        print(f"{'GRAND TOTAL:':<32}${grand_total:<7.2f}")
        print("=" * 40)

        # 6. Pause screen
        input("\n{Press Enter to Go back to the main Menu}: ")

    def update_order_status(self, order_id, new_status):
            """Updates the status of an existing order and saves to JSON."""
            for order in self.orders:
                if order.order_id == order_id:
                    order.status = new_status
                    self._save_orders()  
                    return True
            return False