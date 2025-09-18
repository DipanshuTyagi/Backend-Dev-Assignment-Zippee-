import bcrypt
from app import config
import jwt
from datetime import datetime, timedelta
from app.database import db_session
from app.models.user import User

class AuthService:
    @staticmethod
    def authenticate_user(username: str, password: str):
        """Check if user exists and verify password."""
        user = db_session.query(User).filter(User.username == username).first()
        if not user:
            return None
        
        if bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
            return user
        return None

    @staticmethod
    def create_access_token(user_id: int,role:str) -> str:
        """Generate JWT token for authenticated user."""
        expire = datetime.utcnow() + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {"sub": str(user_id), "exp": expire, "role":role}
        token = jwt.encode(payload, config.SECRET_KEY, algorithm=config.ALGORITHM)
        return token

    @staticmethod
    def decode_access_token(token: str):
        """Decode JWT token and return payload."""
        try:
            payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            return None  # Token expired
        except jwt.InvalidTokenError:
            return None  # Invalid token