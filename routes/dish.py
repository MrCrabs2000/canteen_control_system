from flask import Blueprint, render_template, request, redirect
from flask_security import roles_accepted, current_user
from configs.app_configs import db, login_required
from datebase.classes import Dish, Product, AssociationDishProduct


dish_view = Blueprint('dish_view', __name__)

@dish_view.route('/dishes/<dish_id>', methods=['GET', 'POST'])
@login_required
@roles_accepted('user', 'admin', 'cook')
def dishview(dish_id):
    if current_user.roles[0].name == 'user':
        dish = db.session.query(Dish).filter_by(id=dish_id).first()
        products_list = []

        for idd in dish.product_ids:
            productt = db.session.query(Product).filter_by(id=idd).first()
            products_list.append(productt)

        context = {
            'name': current_user.name,
            'surname': current_user.surname,
            'dish': dish,
            'amount_products': len(products_list),
            'products': products_list,
            'product_amounts': dish.product_amounts,
            'role': current_user.roles[0].name
        }
        try:
            return render_template('dishes/dish.html', **context)
        except Exception as e:
            print(f'Ошибка в dish.py: {e}')
        finally:
            db.session.close()
    else:
        if request.method == 'POST':
            dish = db.session.query(Dish).filter_by(id=dish_id).first()

            amount = int(request.form.get('amount'))

            if not amount:
                return redirect(f'/dishes/{dish_id}')

            cook = True
            for association in dish.products:
                product_dish_amount = int(association.product_amount)
                product_amount = int(association.product.amount)
                if amount * product_dish_amount > product_amount:
                    cook = False
                if not cook:
                    break

            if cook:
                dish.amount += amount
                dish.cook_amount += amount
                for association in dish.products:
                    product_dish_amount = int(association.product_amount)
                    product_amount = int(association.product.amount)
                    product_amount -= amount * product_dish_amount
                    association.product.amount = product_amount
                    association.product.spend_amount += amount * product_dish_amount
            else:
                return redirect(f'/dishes/{dish_id}')

            try:
                db.session.commit()
            except Exception:
                db.session.rollback()
            finally:
                db.session.close()

            return redirect(f'/dishes/{dish_id}')
        
        dish = db.session.query(Dish).filter_by(id=dish_id).first()
        products_list = []

        for idd in dish.product_ids:
            productt = db.session.query(Product).filter_by(id=idd).first()
            products_list.append(productt)

        context = {
            'name': current_user.name,
            'surname': current_user.surname,
            'dish': dish,
            'amount_products': len(products_list),
            'products': products_list,
            'product_amounts': dish.product_amounts,
            'role': current_user.roles[0].name
        }
        try:
            return render_template('dishes/dish.html', **context)
        except Exception as e:
            print(f'Ошибка в dish.py: {e}')
        finally:
            db.session.close()
