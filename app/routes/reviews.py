from flask import Blueprint, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import RestaurantReview, Restaurant
from app import db
from sqlalchemy import func

reviews_bp = Blueprint('reviews', __name__)


@reviews_bp.route('/review/restaurant', methods=['POST'])
@login_required
def add_restaurant_review():
    restaurant_id = int(request.form.get('restaurant_id'))
    rating = int(request.form.get('rating'))
    comment = request.form.get('comment', '').strip()

    if rating < 1 or rating > 5:
        flash('Rating must be between 1 and 5.', 'error')
        return redirect(url_for('main.restaurant_menu', restaurant_id=restaurant_id))

    existing = RestaurantReview.query.filter_by(
        user_id=current_user.user_id, restaurant_id=restaurant_id
    ).first()

    if existing:
        existing.rating = rating
        existing.comment = comment
        flash('Your review has been updated!', 'success')
    else:
        review = RestaurantReview(
            user_id=current_user.user_id, restaurant_id=restaurant_id,
            rating=rating, comment=comment
        )
        db.session.add(review)
        flash('Thank you for your review!', 'success')

    db.session.flush()

    avg = RestaurantReview.query.filter_by(restaurant_id=restaurant_id)\
        .with_entities(func.avg(RestaurantReview.rating)).scalar()
    if avg:
        restaurant = Restaurant.query.get(restaurant_id)
        restaurant.rating = round(float(avg), 1)

    db.session.commit()
    return redirect(url_for('main.restaurant_menu', restaurant_id=restaurant_id))
