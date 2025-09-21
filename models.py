from sqlalchemy import Column, Integer, String, ARRAY
from database import Base

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, index=True)
    username = Column(String, unique=True)
    user_email = Column(String, unique=True)
    age = Column(Integer)
    recommendations = Column(ARRAY(String))
    zip = Column(String)

