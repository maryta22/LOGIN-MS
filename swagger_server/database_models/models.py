from datetime import date, datetime  # noqa: F401

from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# Table: User
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(10), nullable=False)

    sales_advisors = relationship("SalesAdvisor", back_populates="user")
    administrators = relationship("Administrator", back_populates="user")

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.phone
        }

# Table: SalesAdvisor
class SalesAdvisor(Base):
    __tablename__ = 'sales_advisor'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_user = Column(Integer, ForeignKey('user.id'), nullable=False)
    state = Column(Integer, nullable=False)

    user = relationship("User", back_populates="sales_advisors")

    def to_dict(self):
        return {
            "id": self.id,
            "id_user": self.id_user,
            "state": self.state,
            "user": self.user.to_dict() if self.user else None
        }

# Table: Administrator
class Administrator(Base):
    __tablename__ = 'administrator'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_user = Column(Integer, ForeignKey('user.id'), nullable=False)
    state = Column(Integer, nullable=False)
    creation_date = Column(Date, nullable=False)
    modification_date = Column(Date, nullable=True)

    user = relationship("User", back_populates="administrators")

    def to_dict(self):
        return {
            "id": self.id,
            "id_user": self.id_user,
            "state": self.state,
            "creation_date": self.creation_date.strftime('%Y-%m-%d'),
            "modification_date": self.modification_date.strftime('%Y-%m-%d') if self.modification_date else None,
            "user": self.user.to_dict() if self.user else None
        }