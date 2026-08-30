class User:
    def __init__(self, user_id, username, password, role="staff", status="Offline"):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.role = role
        self.status = status

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "password": self.password,
            "role": self.role,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            user_id=data.get("user_id"),
            username=data.get("username"),
            password=data.get("password"),
            role=data.get("role", "staff"),
            status=data.get("status", "Offline")
        )