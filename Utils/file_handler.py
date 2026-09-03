import json
import os
import streamlit as st

class FileHandler:

    # Hidden static method to store raw file contents in fast memory cache
    @st.cache_data
    def _cached_read(file_path):
        with open(file_path, "r", encoding='utf-8') as file:
            return json.load(file)

    @staticmethod
    def read_json(file_path, default_structure):
        if not os.path.exists(file_path):
            FileHandler.write_json(file_path, default_structure)
            return default_structure
        
        try:
            # Calls the cached reader instead of reading from the hard drive
            return FileHandler._cached_read(file_path)
            
        except Exception as e:
            # Fallback for empty/broken files
            st.error(f"⚠️ Error reading file: {e}. Using empty data.")
            return default_structure
        
    @staticmethod
    def write_json(file_path, data):
        try:
            folder_name = os.path.dirname(file_path)

            if folder_name:
                os.makedirs(folder_name, exist_ok=True)

            with open(file_path, "w", encoding='utf-8') as file:
                json.dump(data, file, indent=4)
            
            # CRITICAL: Wipe out old cached data so the next read fetches fresh data
            st.cache_data.clear()
            return True
            
        except Exception as e:
            st.error(f"⚠️ Failed to save Data: {e}")
            return False
