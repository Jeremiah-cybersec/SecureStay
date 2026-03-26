import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key-change-later"
    SQLALCHEMY_DATABASE_URI = "sqlite:///securestay.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
