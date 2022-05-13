from datetime import datetime
from gridfs import Collection


class Payment:
    def __init__(self, collection: Collection) -> None:
        self.collection = collection

    def create_payment(self, chat_id: int, user_id: int, amount: float, description='') -> str:
        result = self.collection.insert_one({
            "chat_id": chat_id,
            "user_id": user_id,
            "amount": amount,
            "description": description,
            "closed": False,
            "created_at": datetime.now()
        })
        return result.inserted_id

    def get_opened_payments(self, chat_id: int) -> list:
        return list(self.collection.find({"chat_id": chat_id, "closed": False}))

    def get_payments(self, chat_id: int) -> list:
        return list(self.collection.find({"chat_id": chat_id}).limit(75))

    def close_payments(self, chat_id: int) -> None:
        self.collection.update_many({
            "chat_id": chat_id,
            "closed": False
        }, {
            "$set": {"closed": True}
        })
