from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import mongo
from bson.objectid import ObjectId

class User:
    @staticmethod
    def create(name, email, password):
        user = {
            "name": name,
            "email": email,
            "password_hash": generate_password_hash(password),
            "created_at": datetime.utcnow()
        }
        result = mongo.db.users.insert_one(user)
        return str(result.inserted_id)

    @staticmethod
    def get_by_email(email):
        return mongo.db.users.find_one({"email": email})

    @staticmethod
    def get_by_id(user_id):
        return mongo.db.users.find_one({"_id": ObjectId(user_id)})

    @staticmethod
    def verify_password(user, password):
        return check_password_hash(user['password_hash'], password)

class Video:
    @staticmethod
    def get_active_videos():
        # Returns list of active videos
        return list(mongo.db.videos.find({"is_active": True}, {"_id": 1, "title": 1, "description": 1, "thumbnail_url": 1, "youtube_id": 1}))

    @staticmethod
    def get_by_id(video_id):
        return mongo.db.videos.find_one({"_id": ObjectId(video_id)})
