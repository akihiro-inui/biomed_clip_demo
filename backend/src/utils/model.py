from pydantic import BaseModel
from bson.objectid import ObjectId


class MongoUserDocument(BaseModel):
    _id: ObjectId
    userId: str
    coin: str
    timestamp: str


class MongoChatDocument(BaseModel):
    _id: ObjectId
    userId: str
    content: str
    role: str
    timestamp: str
