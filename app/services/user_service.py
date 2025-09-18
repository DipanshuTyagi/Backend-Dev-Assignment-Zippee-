import bcrypt
from app.models.user import User
from app.database import db_session

class UserService:
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt."""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed.decode("utf-8")

    @staticmethod
    def create_user(username: str, password: str, role: str = "user") -> User:
        """Create and save a new user in the database."""
        # Check if user already exists
        existing_user = db_session.query(User).filter(User.username == username).first()
        if existing_user:
            raise ValueError("Username already exists")
        
        # Hash the password
        hashed_password = UserService.hash_password(password)

        # Create new user object
        new_user = User(username=username, password=hashed_password, role=role)
        db_session.add(new_user)
        try:
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            raise RuntimeError("Failed to register user") from e
        
        return new_user
