from flask import Flask, Blueprint, render_template, request, redirect
from flask_security import login_required, current_user, roles_accepted
from configs.app_configs import db
from datebase.classes import Review, Dish
from datetime import datetime, date


reviews_main = Blueprint('reviews_main', __name__)


@reviews_main.route('/reviews')
@login_required
@roles_accepted('user')
def reviewsmain():
    reviews = db.session.query(Review).filter_by(user_id=current_user.id).all()

    if not reviews:
        reviews = False

    return render_template('reviews_main.html', reviews=reviews)


review_view = Blueprint('review_view', __name__)


@review_view.route('/reviews/<review_id>', methods=["GET", "POST"])
@login_required
@roles_accepted('user')
def reviewview(review_id):
    review = db.session.query(Review).filter_by(id=review_id, user_id=current_user.id).first()

    if not review:
        return redirect('/reviews')

    dishes = db.session.query(Dish).all()

    if request.method == 'GET':
        return render_template('review_detail.html',
                               review=review,
                               dishes=dishes)

    elif request.method == 'POST':
        if request.form.get('methodd') == 'DELETE':
            db.session.delete(review)
            db.session.commit()

            return redirect('/reviews')

        content = request.form.get('content')
        dish_id = request.form.get('dish_id')
        stars = request.form.get('stars')

        if content:
            review.content = content
        if dish_id:
            review.dish_id = dish_id
        if stars:
            review.stars = stars

        review.date = datetime.strptime(str(date.today()), '%Y-%m-%d').date()
        db.session.commit()

        return redirect(f'/reviews/{review.id}')


review_new = Blueprint('review_new', __name__)


@review_new.route('/reviews/new', methods=["GET", "POST"])
@login_required
@roles_accepted('user')
def reviewnew():
    dishes = db.session.query(Dish).all()

    if request.method == 'GET':
        return render_template('review_create.html', dishes=dishes)

    elif request.method == 'POST':
        content = request.form.get('content')
        dish_id = request.form.get('dish_id')
        stars = request.form.get('stars')

        if all([content, dish_id, stars]):
            new_review = Review(
                content=content,
                dish_id=dish_id,
                date=datetime.strptime(str(date.today()), '%Y-%m-%d').date(),
                stars=stars,
                user_id=current_user.id
            )

            db.session.add(new_review)
            db.session.commit()

            return redirect(f'/reviews')
        else:
            return render_template('review_create.html',
                                   dishes=dishes)