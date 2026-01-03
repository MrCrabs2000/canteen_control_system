from sqlalchemy import Column, Integer, String, ForeignKey, JSON, DateTime, Boolean
from sqlalchemy.orm import relationship, declarative_base
from flask_login import UserMixin
from datetime import datetime

table_base = declarative_base()


class DishProduct(table_base):
    __tablename__ = 'dish_products'

    dish_id = Column(Integer, ForeignKey('dishes.id', ondelete='CASCADE'), primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id', ondelete='CASCADE'), primary_key=True)


class AssociationDishMenu(table_base):
    __tablename__ = 'association_dish_menu'

    menu_id = Column(Integer, ForeignKey('menus.id', ondelete='CASCADE'), primary_key=True)
    dish_id = Column(Integer, ForeignKey('dishes.id', ondelete='CASCADE'), primary_key=True)


class User(table_base, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    patronymic = Column(String, nullable=False)
    login = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role = Column(String, default='student')

    reviews = relationship('Review', back_populates='user', cascade='all, delete-orphan')
    student_info = relationship("Info", back_populates="user", cascade='all, delete-orphan')
    history_records = relationship('History', back_populates='user', cascade='all, delete-orphan')


class Info(table_base):
    __tablename__ = 'students_info'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, unique=True)
    allergies = Column(JSON, default=dict)
    abonement = Column(Boolean, default=False)
    preferences = Column(JSON, default=dict)
    balance = Column(Integer, default=0)
    stud_class = Column(String, default='-')

    user = relationship("User", back_populates="student_info")


class Review(table_base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    dish_id = Column(Integer, ForeignKey('dishes.id', ondelete='CASCADE'), nullable=False)
    content = Column(JSON, default=dict)
    date = Column(DateTime, default=datetime.utcnow, nullable=False)
    stars = Column(Integer, nullable=True)

    user = relationship('User', back_populates='reviews')
    dish = relationship('Dish', back_populates='reviews')


class Product(table_base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False, unique=True)
    amount = Column(Integer, nullable=False, default=0)

    dishes = relationship('Dish', secondary='dish_products', back_populates='products')


class History(table_base):
    __tablename__ = 'history'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    breakfast_date = Column(DateTime, nullable=False)
    lunch_date = Column(DateTime, nullable=False)

    user = relationship('User', back_populates='history_records')


class Menu(table_base):
    __tablename__ = 'menus'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    type = Column(String, nullable=False)
    get_amount = Column(Integer, nullable=False, default=0)

    dishes = relationship('Dish', secondary='association_dish_menu', back_populates='menus')


class Dish(table_base):
    __tablename__ = 'dishes'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False, unique=True)
    amount = Column(Integer, nullable=False, default=0)

    products = relationship('Product', secondary='dish_products', back_populates='dishes')
    reviews = relationship('Review', back_populates='dish', cascade='all, delete-orphan')
    menus = relationship('Menu', secondary='association_dish_menu', back_populates='dishes')
