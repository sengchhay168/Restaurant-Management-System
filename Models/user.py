class User:
    def __init__(self, user_id, username, password, role="staff") :
        self.user_id = user_id
        self.username = username
        self.password = password
        self.role = role

    def to_dict(self) :
        return {
            "user_id" : self.user_id,
            "username" : self.username,
            "password" : self.password,
            "role" : self.role
        }
   
    @classmethod
    def from_dict(cls, data) :
        return cls (
            user_id=data["user_id"],
            username=data["username"],
            password=data["password"],
            role=data["role"]
        )
