from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Enum
from app.database import Base, engine
import enum


# Base.metadata.create_all(bind=engine)
# Define available roles for users
class RoleEnum(str, enum.Enum):
    user = "user"
    admin = "admin"

# User model mapped to "users" table
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)  # store hashed password
    role = Column(Enum(RoleEnum), default=RoleEnum.user, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, role={self.role})>"