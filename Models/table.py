class Table:
    def __init__(self, table_id, capacity, is_occupied=False):
        self.table_id = table_id
        self.__capacity = capacity
        self.__is_occupied = is_occupied

    @property
    def capacity(self):
        return self.__capacity

    @property
    def is_occupied(self):
        return self.__is_occupied

    @is_occupied.setter
    def is_occupied(self, value):
        self.__is_occupied = value

    def occupy(self) :
        if self.__is_occupied:
           print("The Table has already taken!")
           return False
        else :
            self.__is_occupied = True
            print(f"[✓] Success: Table {self.table_id} has been successfully assigned to guests.")
            return True
        
    def vacate(self):
        if self.__is_occupied is False:
            # If it's already empty, let the user know!
            print(f"⚠️ Table {self.table_id} is already empty!")
            return False
        else:
            # This is where the actual clearing happens!
            self.__is_occupied = False
            print(f"🧹 Table {self.table_id} has been successfully vacated and cleaned!")
            return True

    def get_details(self):
    # 1. Determine the status text string
        status = "Occupied" if self.__is_occupied else "Available"
    
    # 2. Return the aligned f-string
        return f"Table {self.table_id:<5} | Capacity: {self.capacity:<3} | Status: {status}"
    