from sqlalchemy import Column, Integer, String, ForeignKey, JSON, DateTime, BOOLEAN, ARRAY
from sqlalchemy.orm import relationship, declarative_base

table_base = declarative_base()

class User(table_base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    patronymic = Column(String, nullable=False)
    login = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, default='user')


    reviews = relationship('Review', back_populates='user')
    student_info = relationship("Info", back_populates="user")
    history = relationship('History', back_populates='user')


class Info(table_base):
    __tablename__ = 'students_info'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    alergies = Column(JSON)
    aboniment = Column(BOOLEAN, default=False)
    preferences = Column(JSON)
    balance = Column(Integer, nullable=False, default=0)
    clas = Column(String, default='')

    user = relationship("User", back_populates="student_info")
    product = relationship("Product", back_populates='info')


class Review(table_base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    content = Column(JSON)
    dish_id = Column(Integer, ForeignKey('dishes.id'), nullable=False)
    date = Column(DateTime, nullable=False)
    stars = Column(Integer, nullable=True)

    user = relationship('User', back_populates='reviews')
    dish = relationship('Dish')


class Product(table_base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    amount = Column(Integer, nullable=False, default=0)

    info = relationship('Info', back_populates='product')
    dishes = relationship('Dish', back_populates='productss')


class Dish(table_base):
    __tablename__ = 'dishes'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    products = Column(ARRAY(Integer), nullanle=False)
    amount = Column(Integer, nullable=False, default=0)

    productss = relationship('Product', back_populates='dishes')
    reviews = relationship('Review', back_populates='dish')


class History(table_base):
    __tablename__ = 'history'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    date = Column(DateTime, nullable=False)

    user = relationship('User', back_populates='history')