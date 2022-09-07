from sqlalchemy import Column, String, Integer, ForeignKey
from app.database import Base

class User(Base):
    __tablename__="users"
    id= Column(Integer, primary_key=True, index=True)
    username = Column(String, ForeignKey("accounts.username"))
    name = Column(String, index=True, nullable=True)
    age = Column (Integer, index=True, nullable=True)
    gender = Column (String, index= True, nullable=True)

class Account(Base):
    __tablename__ = "accounts"
    username = Column(String, primary_key=True,index= True)
    email = Column (String, index= True)
    password = Column(String, index= True)

