from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Order, Payment
from app import db
import random

payments_bp = Blueprint('payments', __name__)


@payments_bp.route('/payment/<int:order_id>')
@login_required
def payment_page(order_id):
    order = Order.query.get_or_404(order_id)

    if order.user_id != current_user.user_id:
        flash('Unauthorized.', 'error')
        return redirect(url_for('orders.order_history'))

    payment = Payment.query.filter_by(order_id=order_id).first()

    if payment and payment.payment_status == 'Success':
        flash('Payment already completed.', 'info')
        return redirect(url_for('orders.track_order', order_id=order_id))

    return render_template(
        'payments/payment.html',
        order=order,
        payment=payment
    )


@payments_bp.route('/payment/process', methods=['POST'])
@login_required
def process_payment():
    order_id = int(request.form.get('order_id'))
    payment_mode = request.form.get('payment_mode', 'Cash on Delivery')

    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.user_id:
        flash('Unauthorized.', 'error')
        return redirect(url_for('orders.order_history'))

    payment = Payment.query.filter_by(order_id=order_id).first()

    if not payment:
        payment = Payment(
            payment_mode=payment_mode,
            amount=float(order.total_amount),
            order_id=order_id
        )
        db.session.add(payment)
    else:
        payment.payment_mode = payment_mode

    # Simulate payment processing (90% success rate)
    if payment_mode == 'Cash on Delivery':
        payment.payment_status = 'Success'
        order.order_status = 'Confirmed'
        flash('Order confirmed! Pay on delivery.', 'success')
    else:
        success = random.random() < 0.9
        if success:
            payment.payment_status = 'Success'
            order.order_status = 'Confirmed'
            flash('Payment successful! Your order is confirmed.', 'success')
        else:
            payment.payment_status = 'Failed'
            flash('Payment failed. Please try again.', 'error')
            db.session.commit()
            return redirect(url_for('payments.payment_page', order_id=order_id))

    db.session.commit()
    return redirect(url_for('orders.track_order', order_id=order_id))
