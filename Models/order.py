class Order:
    def __init__(self, order_id, table_id, items, status="pending", total_price=0.0):
        self.order_id = order_id
        self.table_id = table_id
        self.items = items  # This will be a list of dictionaries: [{"item_id": ..., "quantity": ...}]
        self.status = status
        self.total_price = total_price

    def to_dict(self):
        # Convert this order object into a dictionary for JSON saving
        return {
            "order_id" : self.order_id,
            "table_id" : self.table_id,
            "items" : self.items,
            "status" : self.status,
            "total_price" : self.total_price
        }

    @classmethod
    def from_dict(cls, data):
        # Recreate an Order object from a loaded JSON dictionary
        return cls (
            order_id=data["order_id"],
            table_id=data["table_id"],
            items=data["items"],
            status=data["status"],
            total_price=data["total_price"]
        )
    