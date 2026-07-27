import json
import os
from Models.table import Table


class TableService:
    def __init__(self, filename="Data/tables.json"):
        self.filename = filename
        self.tables = []
        self.load_tables()  # Load saved tables as soon as service starts

    def load_tables(self):
        """Reads tables from JSON and converts them into Table objects."""
        if not os.path.exists(self.filename):
            self.tables = []
            return

        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
                self.tables = [
                    Table(
                        item["table_id"], 
                        item["capacity"], 
                        item.get("is_occupied", False)
                    ) 
                    for item in data
                ]
        except Exception as e:
            print(f"⚠️ Warning loading tables: {e}")
            self.tables = []

    def save_tables(self):
        """Saves current table objects back into the JSON file."""
        try:
            # Ensure the folder directory exists before saving
            os.makedirs(os.path.dirname(self.filename), exist_ok=True)
            
            with open(self.filename, "w") as f:
                data = [
                    {
                        "table_id": t.table_id,
                        "capacity": t.capacity,
                        "is_occupied": t.is_occupied
                    }
                    for t in self.tables
                ]
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"❌ Error saving tables: {e}")

    def add_table(self, table_id, capacity):
        for t in self.tables:
            if table_id == t.table_id:
                print(f"❌ Table ID '{table_id}' already exists!")
                return False
        
        new_table = Table(table_id, capacity)
        self.tables.append(new_table)
        self.save_tables()
        print(f"✅ Table '{table_id}' added successfully!")
        return True 

    def find_table(self, table_id):
        for t in self.tables:
            if table_id == t.table_id:
                return t
        print(f"❌ No table found with ID '{table_id}'.")
        return None

    def get_available_tables(self, party_size):
        return [
            t for t in self.tables 
            if not t.is_occupied and t.capacity >= party_size
        ]

    def occupy_table(self, table_id, party_size):
        table = self.find_table(table_id)
        if table is None:
            return 

        # Check capacity first before attempting to occupy
        if party_size > table.capacity:
            print(f"❌ Party size ({party_size}) is too large for Table {table_id} (Capacity: {table.capacity}).")
            return

     
        if table.occupy():
            self.save_tables()

    def vacate_table(self, table_id):
        table = self.find_table(table_id)
        if table is None:
            return 
        
        if table.vacate():
            self.save_tables()

    def update_order_status(self, order_id, new_status):
        """Updates the status of an existing order and saves to JSON."""
        for order in self.orders:
            if order.order_id == order_id:
                order.status = new_status
                self.save_orders()  
                return True
        return False