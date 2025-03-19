import os
from pathlib import Path

basedir = Path(__file__).parent

class Config:
    """Application configuration settings"""
    
    # Secret key for session management and CSRF protection
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'b1aef80f4d7e1c8f20a7063f8304eac3'
    
    # Database configuration - using SQLite for simplicity
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f'sqlite:///{basedir / "app.db"}'
    
    # Disable modification tracking to save resources
    SQLALCHEMY_TRACK_MODIFICATIONS = False