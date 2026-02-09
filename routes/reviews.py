from flask import Flask, Blueprint, render_template, request, redirect
from flask_security import current_user, roles_accepted
from datetime import datetime, date
from configs.app_configs import db, login_required
from datebase.classes import Review, Dish



reviews_main = Blueprint('reviews_main', __name__)

@reviews_main.route('/reviews')
@login_required
@roles_accepted('user', 'cook')
def reviewsmain():
    if current_user.roles[0].name == 'user':
        reviews = db.session.query(Review).filter_by(user_id=current_user.id).all()
    else:
        reviews = db.session.query(Review).all()

    context = {
        'name': current_user.name,
        'surname': current_user.surname,
        'reviews': reviews,
        'current_user': current_user,
    }

    return render_template('reviews/list.html', **context)


review_new = Blueprint('review_new', __name__)

@review_new.route('/reviews/add', methods=["GET", "POST"])
@login_required
@roles_accepted('user')
def reviewnew():
    dishes = db.session.query(Dish).all()
    reviews = db.session.query(Review).filter_by(user_id=current_user.id).all()

    if request.method == 'GET':
        try:
            return redirect(f'/reviews', dishes=dishes, reviews=reviews)
        except Exception as e:
            print(f'Ошибочка в отзывах : {e}')
        finally:
            db.session.close()

    elif request.method == 'POST':
        content = request.form.get('content')
        dish_id = request.form.get('dish_id')

        if all([content, dish_id]):
            new_review = Review(
                content=content,
                dish_id=dish_id,
                date=datetime.strptime(str(date.today()), '%Y-%m-%d').date(),
                user_id=current_user.id
            )

            db.session.add(new_review)

            try:
                db.session.commit()
            except Exception as e:
                print(f'Ошибка при создании отзыва: {e}')
                db.session.rollback()
            finally:
                db.session.close()

            return redirect(f'/reviews')
        else:
            return redirect(f'/reviews')


reviews_del = Blueprint('reviews_del', __name__)

@reviews_del.route('/review/<review_id>/del', methods=['POST'])
@login_required
@roles_accepted('user', 'cook')
def reviewsmain(review_id, dish_id):
    review = db.session.query(Review).filter_by(id=review_id).first()
    try:
        db.session.delete(review)
        return redirect(f'/dishes/{dish_id}')
    except Exception as e:
        print(f'Ошибка при удалении отзыва: {e}')
        return redirect(f'/dishes/{dish_id}')
    finally:
        db.session.close()