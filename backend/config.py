import os
import secrets

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(16)
    # Default to local mongodb if not provided
    MONGO_URI = os.environ.get('MONGO_URI') or "mongodb://ub6lpnqxtds1tpg3dzj6:SMdsWdwP77VJKd8eTKo@b0tyrvejmzg5hfldegkm-mongodb.services.clever-cloud.com:2450/b0tyrvejmzg5hfldegkm"
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or "super-secret-jwt-key"
