from datetime import datetime
from gridfs import Collection


class User:
    def __init__(self, collection: Collection) -> None:
        self.collection = collection

    def user_exists(self, user_id: int) -> bool:
        doc = self.collection.find_one({"user_id": user_id})

        if doc:
            return True
        return False

    def register_user(self, user_id: int, fullname: str) -> str:
        result = self.collection.insert_one({
            "user_id": user_id,
            "fullname": fullname,
            "created_at": datetime.now()
        })
        return result.inserted_id

    def get_users_by_ids(self, user_ids: list) -> list:
        result = self.collection.find({
            "user_id": {
                "$in": user_ids
            }
        })

        return list(result)
