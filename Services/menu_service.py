from Models import menu_item 
from Utils import file_handler

file = file_handler.FileHandler()
menu = menu_item.MenuItem

class MenuService:
    def __init__(self, data_file="Data/menu.json"):
        self.data_file = data_file
        self.menu_items = self._load_menu()

    def _load_menu(self):
        """Loads data from JSON and converts them into MenuItem objects."""

        raw_data = file.read_json(self.data_file, [])
        converted_item = []

        for item_dict in raw_data :
            menu_obj = menu.from_dict(item_dict)
            converted_item.append(menu_obj) 
        return converted_item

    def _save_menu(self):
      dict_list =[]

      for item in self.menu_items :
         item_as_dictionary = item.to_dict() 
         dict_list.append(item_as_dictionary)
            
      file.write_json(self.data_file, dict_list)

    def add_item(self, item_id, name, category, price):
        """Adds a new item to the menu."""

        for item in self.menu_items :
            if item.item_id == item_id :
                print("No duplicates allowed!")
                return False
                
        item = menu(item_id, name, category, price)
        self.menu_items.append(item)
        self._save_menu()
        return True

    def get_all_items(self):
        """Returns the list of all menu items."""
        if not self.menu_items:
            return []  # Return an empty list so the program doesn't crash
        
        return self.menu_items
     
    def search_items(self, keyword):
        """Searches items by matching keyword against name or category (case-insensitive)."""

        if not self.menu_items:
            print("The menu is empty! There is nothing to search.")
            return []
        
        clean_keyword = keyword.lower()

        results = []

        for item in self.menu_items:
            if clean_keyword in item.name.lower() or clean_keyword in item.category.lower() :
                results.append(item)
        return results
    
    def delete_item(self, item_id):
        """Deletes an item from the menu by its ID."""

        if not self.menu_items: 
            print("The menu is currently empty! Please add some items first.")
            return False
        
        for item in self.menu_items:
            if item.item_id == item_id:
                self.menu_items.remove(item)
                self._save_menu()
                return True
        print("No items found!")
        return False
    
    def get_item(self, item_id):
        """Finds and returns a MenuItem by its ID."""
        for item in self.menu_items:
            if item.item_id == item_id:
                return item
        return None