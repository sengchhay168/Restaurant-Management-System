class MenuItem :
    def __init__(self, item_id, name, category, price):
        self.item_id = item_id
        self.name = name
        self.category = category
        self.price = price
    
    def to_dict(self):

        return {
            "item_id" : self.item_id, 
            "name" : self.name,
            "category" : self.category,
            "price" : self.price
        }
    
    @classmethod
    def from_dict(cls, data) :
        return cls (
            item_id=data["item_id"],
            name=data["name"],
            category=data["category"],
            price=data["price"]
        )
