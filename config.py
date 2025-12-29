import os
from dotenv import load_dotenv


load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

  
    DB_PATH = os.path.join(BASE_DIR, "instance", "assignment_finder.db")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

   
    UPLOAD_FOLDER = os.path.join(
        BASE_DIR, "static", "uploads", "solutions"
    )
    ALLOWED_EXTENSIONS = {"pdf"}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  

  
    DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"
