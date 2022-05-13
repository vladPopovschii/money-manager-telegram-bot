from datetime import datetime
from bson import ObjectId
from gridfs import Collection

from utils import calc_totals


class Total:
    def __init__(self, collection: Collection) -> None:
        self.collection = collection

    def create_total(self, chat_id: int, payments) -> str:
        total_map = calc_totals(payments)
        string_key_map = {}

        for int_key in total_map:
            string_key_map[str(int_key)] = total_map[int_key]

        result = self.collection.insert_one({
            "chat_id": chat_id,
            "total_map": string_key_map,
            "created_at": datetime.now()
        })
        return result.inserted_id

    def get_total(self, chat_id: int, id: int) -> dict:
        result = self.collection.find_one({
            "chat_id": chat_id,
            "_id": ObjectId(id)
        })
        return result["total_map"]
