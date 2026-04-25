from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.models import Order, OrderItem, Cart, CartItem, Payment, Delivery, DeliveryPerson, Coupon, OrderCoupon
from app import db
from datetime import datetime

orders_bp = Blueprint('orders', __name__)


@orders_bp.route('/checkout')
@login_required
def checkout():
    cart = Cart.query.filter_by(user_id=current_user.user_id, status='ACTIVE').first()
    if not cart:
        flash('Your cart is empty.', 'error')
        return redirect(url_for('cart.view_cart'))

    items = CartItem.query.filter_by(cart_id=cart.cart_id).all()
    if not items:
        flash('Your cart is empty.', 'error')
        return redirect(url_for('cart.view_cart'))

    cart_items = []
    subtotal = 0
    restaurant = None

    for ci in items:
        item_total = float(ci.menu_item.price) * ci.quantity
        cart_items.append({
            'item': ci.menu_item,
            'quantity': ci.quantity,
            'total': item_total
        })
        subtotal += item_total
        if not restaurant:
            restaurant = ci.menu_item.restaurant

    coupons = Coupon.query.filter_by(status='ACTIVE').all()

    return render_template(
        'orders/checkout.html',
        cart_items=cart_items,
        subtotal=subtotal,
        restaurant=restaurant,
        coupons=coupons
    )


@orders_bp.route('/order/place', methods=['POST'])
@login_required
def place_order():
    cart = Cart.query.filter_by(user_id=current_user.user_id, status='ACTIVE').first()
    if not cart:
        flash('Your cart is empty.', 'error')
        return redirect(url_for('cart.view_cart'))

    items = CartItem.query.filter_by(cart_id=cart.cart_id).all()
    if not items:
        flash('Your cart is empty.', 'error')
        return redirect(url_for('cart.view_cart'))

    # Calculate totals
    subtotal = sum(float(ci.menu_item.price) * ci.quantity for ci in items)
    restaurant_id = items[0].menu_item.restaurant_id

    # Get form data
    delivery_address = request.form.get('delivery_address', current_user.address or '')
    special_instructions = request.form.get('special_instructions', '')
    coupon_id = request.form.get('coupon_id')
    payment_mode = request.form.get('payment_mode', 'Cash on Delivery')

    # Apply coupon discount
    discount_amount = 0
    coupon = None
    if coupon_id:
        coupon = Coupon.query.get(int(coupon_id))
        if coupon and coupon.status == 'ACTIVE':
            discount_amount = min(
                subtotal * float(coupon.discount_percentage) / 100,
                float(coupon.max_discount)
            )

    total_amount = subtotal - discount_amount

    # Create order
    order = Order(
        total_amount=total_amount,
        discount_amount=discount_amount,
        order_status='Placed',
        user_id=current_user.user_id,
        restaurant_id=restaurant_id,
        delivery_address=delivery_address,
        special_instructions=special_instructions
    )
    db.session.add(order)
    db.session.flush()

    # Create order items
    for ci in items:
        order_item = OrderItem(
            quantity=ci.quantity,
            price=float(ci.menu_item.price),
            order_id=order.order_id,
            item_id=ci.item_id
        )
        db.session.add(order_item)

    # Create payment record
    payment = Payment(
        payment_mode=payment_mode,
        payment_status='Pending',
        amount=total_amount,
        order_id=order.order_id
    )
    db.session.add(payment)

    # Track coupon usage
    if coupon:
        order_coupon = OrderCoupon(order_id=order.order_id, coupon_id=coupon.coupon_id)
        db.session.add(order_coupon)
        coupon.times_used += 1

    # Assign delivery person
    delivery_person = DeliveryPerson.query.filter_by(status='AVAILABLE').first()
    if delivery_person:
        delivery = Delivery(
            order_id=order.order_id,
            delivery_id=delivery_person.delivery_id,
            delivery_status='ASSIGNED'
        )
        db.session.add(delivery)
        delivery_person.status = 'BUSY'

    # Mark cart as ordered
    cart.status = 'ORDERED'

    db.session.commit()

    # Redirect to payment page
    return redirect(url_for('payments.payment_page', order_id=order.order_id))


@orders_bp.route('/orders')
@login_required
def order_history():
    orders = Order.query.filter_by(user_id=current_user.user_id)\
        .order_by(Order.order_date.desc()).all()

    order_list = []
    for order in orders:
        order_list.append({
            'order': order,
            'items': OrderItem.query.filter_by(order_id=order.order_id).all(),
            'payment': Payment.query.filter_by(order_id=order.order_id).first(),
            'delivery': Delivery.query.filter_by(order_id=order.order_id).first()
        })

    return render_template('orders/history.html', order_list=order_list)


@orders_bp.route('/order/<int:order_id>/track')
@login_required
def track_order(order_id):
    order = Order.query.get_or_404(order_id)

    if order.user_id != current_user.user_id and not current_user.is_admin:
        flash('Unauthorized.', 'error')
        return redirect(url_for('orders.order_history'))

    order_items = OrderItem.query.filter_by(order_id=order_id).all()
    payment = Payment.query.filter_by(order_id=order_id).first()
    delivery = Delivery.query.filter_by(order_id=order_id).first()

    statuses = ['Placed', 'Confirmed', 'Preparing', 'Out for Delivery', 'Delivered']
    current_index = statuses.index(order.order_status) if order.order_status in statuses else 0

    return render_template(
        'orders/tracking.html',
        order=order,
        order_items=order_items,
        payment=payment,
        delivery=delivery,
        statuses=statuses,
        current_index=current_index
    )
