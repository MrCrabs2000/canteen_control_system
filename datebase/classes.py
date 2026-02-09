from flask_security import UserMixin, RoleMixin
from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()


class Role(db.Model, RoleMixin):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String, nullable=False, unique=True)

    users = db.relationship('User', secondary='user_roles', back_populates='roles')


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    surname = db.Column(db.String, nullable=False)
    patronymic = db.Column(db.String, nullable=False)
    login = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    active = db.Column(db.Boolean)
    fs_uniquifier = db.Column(db.String, unique=True)
    current_login_at = db.Column(db.DateTime)
    current_login_ip = db.Column(db.String(100))
    last_login_at = db.Column(db.DateTime)
    last_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.Integer, default=0)
    confirmed_at = db.Column(db.DateTime)

    reviews = db.relationship('Review', back_populates='user', cascade='all, delete-orphan')
    student_info = db.relationship("Info", back_populates="user", uselist=False, cascade='all, delete-orphan')
    history = db.relationship('History', back_populates='user', cascade='all, delete-orphan')
    roles = db.relationship('Role', secondary='user_roles', back_populates='users')
    user_accepted = db.relationship('Menu', secondary='user_menus', back_populates='menu_accepted')


class Info(db.Model):
    __tablename__ = 'students_info'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', name='info_users', ondelete='CASCADE'), nullable=False, unique=True)
    allergies = db.Column(db.JSON)
    abonement = db.Column(db.Date)
    preferences = db.Column(db.JSON)
    balance = db.Column(db.Integer, nullable=False, default=0)
    stud_class = db.Column(db.String, default='-')

    user = db.relationship("User", back_populates="student_info")


class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', name='review_users', ondelete='CASCADE'), nullable=False)
    content = db.Column(db.JSON)
    dish_id = db.Column(db.Integer, db.ForeignKey('dishes.id', name='review_dishes', ondelete='CASCADE'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    stars = db.Column(db.Integer, nullable=True)

    user = db.relationship('User', back_populates='reviews')
    dish = db.relationship('Dish', back_populates='reviews')


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    measurement = db.Column(db.String, nullable=False)
    amount = db.Column(db.Integer, nullable=False, default=0)
    buy_amount = db.Column(db.Integer, nullable=False, default=0)
    spend_amount = db.Column(db.Integer, nullable=False, default=0)

    dishes = db.relationship('AssociationDishProduct', back_populates='product', cascade='all, delete-orphan')
    requisitions = db.relationship('Requisition', back_populates='product', cascade='all, delete-orphan')


class Requisition(db.Model):
    __tablename__ = 'requisitions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', name='requisition_products', ondelete='CASCADE'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id', name='requisition_users', ondelete='CASCADE'), nullable=False)
    amount = db.Column(db.Integer, nullable=False, default=0)
    date = db.Column(db.Date, nullable=False, default=date.today())
    coordination = db.Column(db.Integer, nullable=False, default=0)

    product = db.relationship('Product', back_populates='requisitions')


class Menu(db.Model):
    __tablename__ = 'menus'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    type = db.Column(db.String, nullable=False)
    get_amount = db.Column(db.Integer, nullable=False, default=0)
    date = db.Column(db.Date, nullable=False, default=date.today())
    price = db.Column(db.Integer, nullable=False)

    dishes = db.relationship('Dish', secondary='dish_menu', back_populates='menus')
    menu_accepted = db.relationship('User', secondary='user_menus', back_populates='user_accepted')
    history = db.relationship('History', back_populates='menu', cascade='all, delete-orphan')


class History(db.Model):
    __tablename__ = 'history'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', name='history_users', ondelete='CASCADE'), nullable=False)
    menu_id = db.Column(db.Integer, db.ForeignKey('menus.id', name='history_menus', ondelete='CASCADE'), nullable=False)
    eat_date = db.Column(db.Date, nullable=False)
    type = db.Column(db.String, nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Boolean, nullable=False, default=False)

    user = db.relationship('User', back_populates='history')
    menu = db.relationship('Menu', back_populates='history')


class Dish(db.Model):
    __tablename__ = 'dishes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    amount = db.Column(db.Integer, nullable=False, default=0)
    category = db.Column(db.String, nullable=False)
    cook_amount = db.Column(db.Integer, nullable=False, default=0)
    give_amount = db.Column(db.Integer, nullable=False, default=0)

    products = db.relationship('AssociationDishProduct', back_populates='dish', cascade='all, delete-orphan')
    reviews = db.relationship('Review', back_populates='dish', cascade='all, delete-orphan')
    menus = db.relationship('Menu', secondary='dish_menu', back_populates='dishes')

    CATEGORIES = {
        'breakfasts': 'Завтраки',
        'salads': 'Салаты',
        'soups': 'Супы',
        'main_dishes': 'Основные блюда',
        'drinks': 'Напитки',
        'bread': 'Хлеб'
    }

    @property
    def product_ids(self):
        return [assoc.product_id for assoc in self.products]
    
    @property
    def product_amounts(self):
        return [assoc.product_amount for assoc in self.products]

    @property
    def category_name(self):
        return self.CATEGORIES.get(self.category, self.category)

    @classmethod
    def get_category_name(cls, category):
        return cls.CATEGORIES.get(category, category)


class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    text = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, nullable=False, default=date.today())
    status = db.Column(db.Integer, nullable=False, default=False)
    type = db.Column(db.String, nullable=True)
    warning = db.Column(db.Boolean, nullable=True)

    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id', name='notification_users', ondelete='CASCADE'), nullable=False)
    requisition_id = db.Column(db.Integer, db.ForeignKey('requisitions.id', name='notification_requisitions', ondelete='CASCADE'), nullable=True)


class AssociationDishProduct(db.Model):
    __tablename__ = 'dish_products'

    dish_id = db.Column(db.Integer, db.ForeignKey('dishes.id', name='dishproducts_dishes', ondelete='CASCADE'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', name='dishproducts_products', ondelete='CASCADE'), primary_key=True)
    product_amount = db.Column(db.Integer, nullable=False)

    dish = db.relationship('Dish', back_populates='products')
    product = db.relationship('Product', back_populates='dishes')


class AssociationDishMenu(db.Model):
    __tablename__ = 'dish_menu'

    menu_id = db.Column(db.Integer, db.ForeignKey('menus.id', name='dishmenu_menus', ondelete='CASCADE'), primary_key=True)
    dish_id = db.Column(db.Integer, db.ForeignKey('dishes.id', name='dishmenu_dishes', ondelete='CASCADE'), primary_key=True)


class AssociationUserMenus(db.Model):
    __tablename__ = 'user_menus'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', name='usermenus_users', ondelete='CASCADE'), primary_key=True)
    menu_id = db.Column(db.Integer, db.ForeignKey('menus.id', name='usermenus_menus', ondelete='CASCADE'), primary_key=True)


class AssociationUserRole(db.Model):
    __tablename__ = 'user_roles'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', name='userroles_users', ondelete='CASCADE'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id', name='userroles_roles', ondelete='CASCADE'), primary_key=True)