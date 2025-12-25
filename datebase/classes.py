from sqlalchemy import Column, Integer, String, ForeignKey, JSON, DateTime, BOOLEAN, Table
from sqlalchemy.orm import relationship, declarative_base
from flask_login import UserMixin


table_base = declarative_base()


class User(table_base, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    patronymic = Column(String, nullable=False)
    login = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, default='user')

    reviews = relationship('Review', back_populates='user')
    student_info = relationship("Info", back_populates="user", uselist=False)
    history = relationship('History', back_populates='user')


class Info(table_base):
    __tablename__ = 'students_info'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, unique=True)
    alergies = Column(JSON)
    aboniment = Column(BOOLEAN, default=False)
    preferences = Column(JSON)
    balance = Column(Integer, nullable=False, default=0)
    stud_class = Column(String, default='')

    user = relationship("User", back_populates="student_info")


class Review(table_base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    content = Column(JSON)
    dish_id = Column(Integer, ForeignKey('dishes.id'), nullable=False)
    date = Column(DateTime, nullable=False)
    stars = Column(Integer, nullable=True)

    user = relationship('User', back_populates='reviews')
    dish = relationship('Dish', back_populates='reviews')


class Product(table_base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    amount = Column(Integer, nullable=False, default=0)

    dishes = relationship('Dish', secondary='dish_products', back_populates='products')


class History(table_base):
    __tablename__ = 'history'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    breakfast_date = Column(DateTime, nullable=False)
    lunch_date = Column(DateTime, nullable=False)

    user = relationship('User', back_populates='history')


class AssociationDishMenu(table_base):
    __tablename__ = 'association_dish_menu'

    menu_id = Column(Integer, ForeignKey('menus.id'), primary_key=True)
    dish_id = Column(Integer, ForeignKey('dishes.id'), primary_key=True)


class DishProduct(table_base):
    __tablename__ = 'dish_products'

    dish_id = Column(Integer, ForeignKey('dishes.id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), primary_key=True)


class Menu(table_base):
    __tablename__ = 'menus'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    type = Column(String, nullable=False)
    get_amount = Column(Integer, nullable=False, default=0)

    dishes = relationship('Dish', secondary='association_dish_menu', back_populates='menus')


class Dish(table_base):
    __tablename__ = 'dishes'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    amount = Column(Integer, nullable=False, default=0)


    products = relationship('Product', secondary='dish_products', back_populates='dishes')
    reviews = relationship('Review', back_populates='dish')
    menus = relationship('Menu', secondary='association_dish_menu', back_populates='dishes')