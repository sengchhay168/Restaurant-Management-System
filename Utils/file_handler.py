import json
import os

class FileHandler :

    @staticmethod
    def read_json(file_path, default_structure) :

        if not os.path.exists(file_path):

            FileHandler.write_json(file_path, default_structure)
            return default_structure
        
        try :
            with open(file_path, "r", encoding='utf-8') as file :

                return json.load(file)
            
        except :

            print("⚠️ Error reading the file. Using empty data.")
            return default_structure
        
    @staticmethod
    def write_json(file_path, data) :
        try :
            folder_name = os.path.dirname(file_path)

            if folder_name :
                os.makedirs(folder_name, exist_ok=True)

            with open(file_path, "w", encoding='utf-8') as file:
                json.dump(data, file, indent=4)
            return True
        except :

            print("⚠️ Failed to save Data!")
            return False
        