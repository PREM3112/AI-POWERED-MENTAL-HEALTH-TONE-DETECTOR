import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DATABASE_PATH = 'database/users.db'
    
    # Model configuration
    MODEL_NAME = "j-hartmann/emotion-english-distilroberta-base"
    MAX_TEXT_LENGTH = 512
    
    # Session configuration
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour