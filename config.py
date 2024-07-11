import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'b1aef80f4d7e1c8f20a7063f8304eac3'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres:92473Vas@localhost/durak_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
