from sqlalchemy import Column, Integer, String, JSON
from database import Base

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, index=True, nullable=False)
    user_name = Column(String, unique=True, nullable=False)
    user_email = Column(String, unique=True, nullable=False)
    age = Column(Integer)
    recommendations = Column(JSON, nullable=False)
    zip = Column(String)

