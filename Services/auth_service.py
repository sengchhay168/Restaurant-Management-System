import os
import json
import bcrypt
from Models.user import User


def _hash_password(plain_password):
    """Hash a plaintext password for storage. Never store raw passwords."""
    return bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def _looks_like_bcrypt_hash(value):
    """bcrypt hashes always start with one of these prefixes."""
    return isinstance(value, str) and value.startswith(("$2a$", "$2b$", "$2y$"))


def _check_password(plain_password, stored_password):
    """
    Verify a password against what's stored. Handles both:
    - New-style bcrypt hashes (the normal case going forward)
    - Legacy plaintext passwords left over from before hashing was added
      (so existing accounts don't get locked out; see login_user, which
      upgrades a legacy password to a proper hash the moment it verifies).
    """
    if _looks_like_bcrypt_hash(stored_password):
        try:
            return bcrypt.checkpw(plain_password.encode("utf-8"), stored_password.encode("utf-8"))
        except ValueError:
            return False
    # Legacy plaintext fallback (only reached for accounts created before hashing existed)
    return plain_password == stored_password


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
        user_id = (user_id or "").strip()
        username = (username or "").strip()
        password = password or ""

        if not user_id or not username:
            print("❌ User ID and Username cannot be empty!")
            return False

        if len(password) < 4:
            print("❌ Password must be at least 4 characters long!")
            return False

        # SECURITY: role is intentionally not trusted from arbitrary external
        # input here beyond "staff"/"admin" — callers (e.g. the public
        # registration form) should never pass anything but "staff" for a
        # self-service signup. See app.py, where the role selector was
        # removed from the public registration form for this reason.
        if role not in ("staff", "admin"):
            role = "staff"

        for u in self.users:
            if u.user_id == user_id or u.username == username:
                print("❌ User ID or Username already exists!")
                return False

        new_user = User(user_id, username, _hash_password(password), role)
        self.users.append(new_user)

        # Save updated list to file
        return self.save_users()

    def login_user(self, username, password):
        clean_user = username.strip() if username else ""
        clean_pass = password.strip() if password else ""
        for u in self.users:
            if clean_user == u.username and _check_password(clean_pass, u.password):
                # If this account still has a legacy plaintext password,
                # transparently upgrade it to a bcrypt hash now that we've
                # verified it, so it's never stored in plaintext again.
                if not _looks_like_bcrypt_hash(u.password):
                    u.password = _hash_password(clean_pass)
                    self.save_users()
                self.current_user = u
                return True
        return False

    def logout(self):
        """Logs out the current user."""
        if self.current_user:
            print(f"Goodbye, {self.current_user.username}!")
            self.current_user = None
        else:
            print("No user is currently logged in.")

    def get_current_role(self):
        if self.current_user:
            return self.current_user.role.lower()
        return None

    def get_all_users(self):
        """Returns all users as dicts, with password hashes stripped out —
        this is used to populate UI (e.g. the admin user-status monitor),
        which should never need or see password data at all."""
        if not os.path.exists(self.data_file):
            return []
        with open(self.data_file, "r") as f:
            data = json.load(f)
        for user in data:
            user.pop("password", None)
        return data

    def count_admins(self):
        """Used to stop the last admin account from being demoted, which
        would otherwise lock everyone out of admin-only features with no
        way back in short of editing the JSON file by hand."""
        return sum(1 for u in self.users if u.role == "admin")

    def set_user_role(self, username, new_role):
        """
        Promotes a staff account to admin, or demotes an admin back to
        staff. Returns (success: bool, message: str) so the caller can show
        a clear reason on failure rather than just silently doing nothing.
        """
        if new_role not in ("staff", "admin"):
            return False, "Invalid role."

        target = next((u for u in self.users if u.username == username), None)
        if not target:
            return False, "User not found."

        if target.role == new_role:
            return False, f"{username} is already {new_role}."

        if target.role == "admin" and new_role == "staff" and self.count_admins() <= 1:
            return False, "Can't demote the only remaining admin — promote someone else first."

        target.role = new_role
        if self.save_users():
            return True, f"{username} is now {new_role}."
        return False, "Failed to save the role change."

    def update_user_status(self, username, status):
        if not os.path.exists(self.data_file):
            return
        with open(self.data_file, "r") as f:
            users = json.load(f)
        for user in users:
            if user.get("username") == username:
                user["status"] = status
        with open(self.data_file, "w") as f:
            json.dump(users, f, indent=4)
        # Keep the in-memory copy consistent too
        for u in self.users:
            if u.username == username:
                u.status = status