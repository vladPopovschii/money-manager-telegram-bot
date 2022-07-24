from datetime import datetime
from gridfs import Collection


class Chat:
    def __init__(self, collection: Collection) -> None:
        self.collection = collection

    def chat_exists(self, chat_id: int, user_id: int) -> bool:
        doc = self.collection.find_one(
            {"user_id": user_id, "chat_id": chat_id})

        if doc:
            return True
        return False

    def register_chat(self, chat_id: int, user_id: int) -> str:
        result = self.collection.insert_one({
            "chat_id": chat_id,
            "user_id": user_id,
            "created_at": datetime.now()
        })
        return result.inserted_id

    def get_users(self, chat_id: int) -> list:
        cursor = self.collection.find({"chat_id": chat_id}).limit(100)
        return list(cursor)
