from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import (User, Restaurant, MenuItem, Category, Order, OrderItem,
                        Payment, Delivery, DeliveryPerson, Coupon)
from app import db
from functools import wraps
from datetime import datetime

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def admin_required(f):
    @wraps(f)
    @login_required
    def decorated(*args, **kwargs):
        if not current_user.is_admin:
            flash('Admin access required.', 'error')
            return redirect(url_for('main.home'))
        return f(*args, **kwargs)
    return decorated


@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    stats = {
        'users': User.query.count(),
        'restaurants': Restaurant.query.count(),
        'orders': Order.query.count(),
        'revenue': float(db.session.query(db.func.coalesce(
            db.func.sum(Order.total_amount), 0
        )).filter(Order.order_status != 'Cancelled').scalar()),
        'pending_orders': Order.query.filter(
            Order.order_status.in_(['Placed', 'Confirmed', 'Preparing'])
        ).count(),
        'active_deliveries': Delivery.query.filter(
            Delivery.delivery_status.in_(['ASSIGNED', 'PICKED', 'IN_TRANSIT'])
        ).count()
    }
    recent_orders = Order.query.order_by(Order.order_date.desc()).limit(10).all()
    return render_template('admin/dashboard.html', stats=stats, recent_orders=recent_orders)


@admin_bp.route('/users')
@admin_required
def manage_users():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=users)


@admin_bp.route('/users/delete/<int:user_id>', methods=['POST'])
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.is_admin:
        flash('Cannot delete admin user.', 'error')
    else:
        db.session.delete(user)
        db.session.commit()
        flash('User deleted.', 'success')
    return redirect(url_for('admin.manage_users'))


@admin_bp.route('/restaurants')
@admin_required
def manage_restaurants():
    restaurants = Restaurant.query.all()
    return render_template('admin/restaurants.html', restaurants=restaurants)


@admin_bp.route('/restaurants/add', methods=['POST'])
@admin_required
def add_restaurant():
    r = Restaurant(
        name=request.form['name'],
        location=request.form['location'],
        cuisine_type=request.form.get('cuisine_type', ''),
        description=request.form.get('description', ''),
        delivery_time=request.form.get('delivery_time', '30-45 min')
    )
    db.session.add(r)
    db.session.commit()
    flash('Restaurant added.', 'success')
    return redirect(url_for('admin.manage_restaurants'))


@admin_bp.route('/restaurants/delete/<int:rid>', methods=['POST'])
@admin_required
def delete_restaurant(rid):
    r = Restaurant.query.get_or_404(rid)
    db.session.delete(r)
    db.session.commit()
    flash('Restaurant deleted.', 'success')
    return redirect(url_for('admin.manage_restaurants'))


@admin_bp.route('/menu-items')
@admin_required
def manage_menu_items():
    items = MenuItem.query.all()
    restaurants = Restaurant.query.all()
    categories = Category.query.all()
    return render_template('admin/menu_items.html', items=items,
                           restaurants=restaurants, categories=categories)


@admin_bp.route('/menu-items/add', methods=['POST'])
@admin_required
def add_menu_item():
    item = MenuItem(
        item_name=request.form['item_name'],
        price=float(request.form['price']),
        description=request.form.get('description', ''),
        restaurant_id=int(request.form['restaurant_id']),
        category_id=int(request.form['category_id'])
    )
    db.session.add(item)
    db.session.commit()
    flash('Menu item added.', 'success')
    return redirect(url_for('admin.manage_menu_items'))


@admin_bp.route('/menu-items/delete/<int:iid>', methods=['POST'])
@admin_required
def delete_menu_item(iid):
    item = MenuItem.query.get_or_404(iid)
    db.session.delete(item)
    db.session.commit()
    flash('Menu item deleted.', 'success')
    return redirect(url_for('admin.manage_menu_items'))


@admin_bp.route('/categories')
@admin_required
def manage_categories():
    categories = Category.query.all()
    return render_template('admin/categories.html', categories=categories)


@admin_bp.route('/categories/add', methods=['POST'])
@admin_required
def add_category():
    cat = Category(
        name=request.form['name'],
        description=request.form.get('description', ''),
        icon=request.form.get('icon', '🍽️')
    )
    db.session.add(cat)
    db.session.commit()
    flash('Category added.', 'success')
    return redirect(url_for('admin.manage_categories'))


@admin_bp.route('/categories/delete/<int:cid>', methods=['POST'])
@admin_required
def delete_category(cid):
    cat = Category.query.get_or_404(cid)
    if cat.menu_items:
        flash('Cannot delete category with menu items.', 'error')
    else:
        db.session.delete(cat)
        db.session.commit()
        flash('Category deleted.', 'success')
    return redirect(url_for('admin.manage_categories'))


@admin_bp.route('/coupons')
@admin_required
def manage_coupons():
    coupons = Coupon.query.all()
    return render_template('admin/coupons.html', coupons=coupons)


@admin_bp.route('/coupons/add', methods=['POST'])
@admin_required
def add_coupon():
    c = Coupon(
        code=request.form['code'].upper(),
        discount_percentage=float(request.form['discount_percentage']),
        min_order_amount=float(request.form.get('min_order_amount', 0)),
        max_discount=float(request.form.get('max_discount', 999)),
        expiry_date=datetime.strptime(request.form['expiry_date'], '%Y-%m-%d').date(),
        usage_limit=int(request.form.get('usage_limit', 100))
    )
    db.session.add(c)
    db.session.commit()
    flash('Coupon added.', 'success')
    return redirect(url_for('admin.manage_coupons'))


@admin_bp.route('/coupons/delete/<int:cid>', methods=['POST'])
@admin_required
def delete_coupon(cid):
    c = Coupon.query.get_or_404(cid)
    db.session.delete(c)
    db.session.commit()
    flash('Coupon deleted.', 'success')
    return redirect(url_for('admin.manage_coupons'))


@admin_bp.route('/orders')
@admin_required
def manage_orders():
    orders = Order.query.order_by(Order.order_date.desc()).all()
    return render_template('admin/orders.html', orders=orders)


@admin_bp.route('/orders/update-status/<int:oid>', methods=['POST'])
@admin_required
def update_order_status(oid):
    order = Order.query.get_or_404(oid)
    new_status = request.form['status']
    order.order_status = new_status

    # Update delivery status accordingly
    delivery = Delivery.query.filter_by(order_id=oid).first()
    if delivery:
        if new_status == 'Preparing':
            delivery.delivery_status = 'ASSIGNED'
        elif new_status == 'Out for Delivery':
            delivery.delivery_status = 'IN_TRANSIT'
            delivery.picked_time = datetime.utcnow()
        elif new_status == 'Delivered':
            delivery.delivery_status = 'DELIVERED'
            delivery.delivered_time = datetime.utcnow()
            if delivery.delivery_person:
                delivery.delivery_person.status = 'AVAILABLE'

    db.session.commit()
    flash(f'Order #{oid} status updated to {new_status}.', 'success')
    return redirect(url_for('admin.manage_orders'))


@admin_bp.route('/delivery')
@admin_required
def manage_delivery():
    persons = DeliveryPerson.query.all()
    active = Delivery.query.filter(
        Delivery.delivery_status.in_(['ASSIGNED', 'PICKED', 'IN_TRANSIT'])
    ).all()
    return render_template('admin/delivery.html', persons=persons, active=active)


@admin_bp.route('/delivery/add', methods=['POST'])
@admin_required
def add_delivery_person():
    dp = DeliveryPerson(
        name=request.form['name'],
        phone=request.form['phone'],
        vehicle_type=request.form.get('vehicle_type', 'Bike')
    )
    db.session.add(dp)
    db.session.commit()
    flash('Delivery person added.', 'success')
    return redirect(url_for('admin.manage_delivery'))
