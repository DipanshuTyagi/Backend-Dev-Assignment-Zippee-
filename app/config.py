import os

from dotenv import load_dotenv


load_dotenv('.env')
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "../data/app.db")

SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH}"
SQLALCHEMY_TRACK_MODIFICATIONS = False


SECRET_KEY = os.getenv('SECRET_KEY')  # change to env variable in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60