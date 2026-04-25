from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models import Cart, CartItem, MenuItem, Coupon
from app import db
from datetime import date

cart_bp = Blueprint('cart', __name__)


def get_or_create_cart(user_id):
    """Get the active cart for a user, or create one."""
    cart = Cart.query.filter_by(user_id=user_id, status='ACTIVE').first()
    if not cart:
        cart = Cart(user_id=user_id, status='ACTIVE')
        db.session.add(cart)
        db.session.commit()
    return cart


@cart_bp.route('/cart')
@login_required
def view_cart():
    cart = Cart.query.filter_by(user_id=current_user.user_id, status='ACTIVE').first()
    cart_items = []
    subtotal = 0
    restaurant = None

    if cart:
        items = CartItem.query.filter_by(cart_id=cart.cart_id).all()
        for ci in items:
            item_total = float(ci.menu_item.price) * ci.quantity
            cart_items.append({
                'cart_item_id': ci.cart_item_id,
                'item': ci.menu_item,
                'quantity': ci.quantity,
                'total': item_total
            })
            subtotal += item_total
            if not restaurant:
                restaurant = ci.menu_item.restaurant

    return render_template(
        'cart/cart.html',
        cart_items=cart_items,
        subtotal=subtotal,
        restaurant=restaurant
    )


@cart_bp.route('/cart/add', methods=['POST'])
@login_required
def add_to_cart():
    data = request.get_json() if request.is_json else request.form
    item_id = int(data.get('item_id'))
    quantity = int(data.get('quantity', 1))

    menu_item = MenuItem.query.get_or_404(item_id)
    cart = get_or_create_cart(current_user.user_id)

    # Multi-restaurant ordering is now allowed, so we skip the restaurant check.

    # Check if item already in cart
    cart_item = CartItem.query.filter_by(cart_id=cart.cart_id, item_id=item_id).first()

    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(cart_id=cart.cart_id, item_id=item_id, quantity=quantity)
        db.session.add(cart_item)

    db.session.commit()

    # Get updated cart count
    count = CartItem.query.filter_by(cart_id=cart.cart_id).count()

    if request.is_json:
        return jsonify({'success': True, 'message': f'{menu_item.item_name} added to cart!', 'cart_count': count})

    flash(f'{menu_item.item_name} added to cart!', 'success')
    return redirect(request.referrer or url_for('main.home'))


@cart_bp.route('/cart/update', methods=['POST'])
@login_required
def update_cart():
    data = request.get_json() if request.is_json else request.form
    cart_item_id = int(data.get('cart_item_id'))
    quantity = int(data.get('quantity', 1))

    cart_item = CartItem.query.get_or_404(cart_item_id)

    # Verify ownership
    if cart_item.cart.user_id != current_user.user_id:
        if request.is_json:
            return jsonify({'success': False, 'message': 'Unauthorized'}), 403
        flash('Unauthorized.', 'error')
        return redirect(url_for('cart.view_cart'))

    if quantity <= 0:
        db.session.delete(cart_item)
    else:
        cart_item.quantity = quantity

    db.session.commit()

    # Recalculate totals
    cart = Cart.query.filter_by(user_id=current_user.user_id, status='ACTIVE').first()
    subtotal = 0
    count = 0
    if cart:
        items = CartItem.query.filter_by(cart_id=cart.cart_id).all()
        count = len(items)
        for ci in items:
            subtotal += float(ci.menu_item.price) * ci.quantity

    if request.is_json:
        return jsonify({
            'success': True,
            'subtotal': subtotal,
            'cart_count': count,
            'item_total': float(cart_item.menu_item.price) * quantity if quantity > 0 else 0
        })

    return redirect(url_for('cart.view_cart'))


@cart_bp.route('/cart/remove', methods=['POST'])
@login_required
def remove_from_cart():
    data = request.get_json() if request.is_json else request.form
    cart_item_id = int(data.get('cart_item_id'))

    cart_item = CartItem.query.get_or_404(cart_item_id)

    if cart_item.cart.user_id != current_user.user_id:
        if request.is_json:
            return jsonify({'success': False, 'message': 'Unauthorized'}), 403
        flash('Unauthorized.', 'error')
        return redirect(url_for('cart.view_cart'))

    db.session.delete(cart_item)
    db.session.commit()

    cart = Cart.query.filter_by(user_id=current_user.user_id, status='ACTIVE').first()
    subtotal = 0
    count = 0
    if cart:
        items = CartItem.query.filter_by(cart_id=cart.cart_id).all()
        count = len(items)
        for ci in items:
            subtotal += float(ci.menu_item.price) * ci.quantity

    if request.is_json:
        return jsonify({'success': True, 'subtotal': subtotal, 'cart_count': count})

    flash('Item removed from cart.', 'info')
    return redirect(url_for('cart.view_cart'))


@cart_bp.route('/cart/clear', methods=['POST'])
@login_required
def clear_cart():
    cart = Cart.query.filter_by(user_id=current_user.user_id, status='ACTIVE').first()
    if cart:
        CartItem.query.filter_by(cart_id=cart.cart_id).delete()
        db.session.commit()

    if request.is_json:
        return jsonify({'success': True, 'cart_count': 0})

    flash('Cart cleared.', 'info')
    return redirect(url_for('cart.view_cart'))


@cart_bp.route('/cart/apply-coupon', methods=['POST'])
@login_required
def apply_coupon():
    data = request.get_json() if request.is_json else request.form
    code = data.get('code', '').strip().upper()

    if not code:
        return jsonify({'success': False, 'message': 'Please enter a coupon code.'})

    coupon = Coupon.query.filter_by(code=code, status='ACTIVE').first()

    if not coupon:
        return jsonify({'success': False, 'message': 'Invalid coupon code.'})

    if coupon.expiry_date < date.today():
        return jsonify({'success': False, 'message': 'This coupon has expired.'})

    if coupon.times_used >= coupon.usage_limit:
        return jsonify({'success': False, 'message': 'This coupon has reached its usage limit.'})

    # Calculate cart subtotal
    cart = Cart.query.filter_by(user_id=current_user.user_id, status='ACTIVE').first()
    if not cart:
        return jsonify({'success': False, 'message': 'Your cart is empty.'})

    items = CartItem.query.filter_by(cart_id=cart.cart_id).all()
    subtotal = sum(float(ci.menu_item.price) * ci.quantity for ci in items)

    if subtotal < float(coupon.min_order_amount):
        return jsonify({
            'success': False,
            'message': f'Minimum order amount is ₹{coupon.min_order_amount}.'
        })

    discount = min(subtotal * float(coupon.discount_percentage) / 100, float(coupon.max_discount))

    return jsonify({
        'success': True,
        'message': f'Coupon applied! You save ₹{discount:.2f}',
        'discount': discount,
        'coupon_id': coupon.coupon_id,
        'discount_percentage': float(coupon.discount_percentage)
    })
