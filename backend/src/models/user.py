from sqlalchemy import Column, Integer, String, TIMESTAMP
from src.db.db import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    created_at = Column(TIMESTAMP, default=datetime.utcnow)


    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"
    