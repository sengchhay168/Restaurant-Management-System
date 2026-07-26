import os
import json
from Models.user import User

class AuthService:
    def __init__(self, data_file="Data/users.json"):
        # Match attribute name to self.data_file everywhere
        self.data_file = data_file
        self.users = []
        self.current_user = None
        self.load_users()

    def load_users(self):
        """Loads users from JSON file using User.from_dict()"""
        if not os.path.exists(self.data_file):
            self.users = []
            return

        try:
            with open(self.data_file, "r") as f:
                data = json.load(f)
                # Convert dictionary objects back to User instances
                self.users = [User.from_dict(item) for item in data]
        except Exception as e:
            print(f"⚠️ Error loading users: {e}")
            self.users = []

    def save_users(self):
        """Saves current User objects using u.to_dict()"""
        try:
            # Ensure the directory exists
            folder = os.path.dirname(self.data_file)
            if folder:
                os.makedirs(folder, exist_ok=True)

            with open(self.data_file, "w") as f:
                data = [u.to_dict() for u in self.users]
                json.dump(data, f, indent=4)
                return True
        except Exception as e:
            print(f"⚠️ Failed to save Data! Reason: {type(e).__name__} - {e}")
            return False

    def register_user(self, user_id, username, password, role="staff"):
        """Registers a new user and saves to file."""
        for u in self.users:
            if u.user_id == user_id or u.username == username:
                print("❌ User ID or Username already exists!")
                return False

        new_user = User(user_id, username, password, role)
        self.users.append(new_user)
        
        # Save updated list to file
        return self.save_users()

    def login_user(self, username, password):
        """Logs in a user by verifying username and password."""
        for u in self.users:
            if username == u.username and password == u.password:
                self.current_user = u
                print(f"Welcome Back! {username}.")
                return True
        print("Invalid Username or Password!")
        return False
    
    def logout(self):
        """Logs out the current user."""
        if self.current_user:
            print(f"Goodbye, {self.current_user.username}!")
            self.current_user = None
        else:
            print("No user is currently logged in.")