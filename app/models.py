from app import db
from flask_login import UserMixin
from datetime import datetime


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    carts = db.relationship('Cart', backref='user', lazy=True)
    orders = db.relationship('Order', backref='user', lazy=True)
    reviews = db.relationship('RestaurantReview', backref='user', lazy=True)

    def get_id(self):
        return str(self.user_id)


class Restaurant(db.Model):
    __tablename__ = 'restaurants'

    restaurant_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.Numeric(2, 1), default=0.0)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(500))
    cuisine_type = db.Column(db.String(100))
    delivery_time = db.Column(db.String(50), default='30-45 min')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    menu_items = db.relationship('MenuItem', backref='restaurant', lazy=True)
    orders = db.relationship('Order', backref='restaurant', lazy=True)
    reviews = db.relationship('RestaurantReview', backref='restaurant', lazy=True)


class Category(db.Model):
    __tablename__ = 'categories'

    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    icon = db.Column(db.String(50), default='🍽️')

    # Relationships
    menu_items = db.relationship('MenuItem', backref='category', lazy=True)


class MenuItem(db.Model):
    __tablename__ = 'menu_items'

    item_id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(500))
    is_available = db.Column(db.Boolean, default=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.restaurant_id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Cart(db.Model):
    __tablename__ = 'carts'

    cart_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.Enum('ACTIVE', 'ORDERED'), default='ACTIVE')

    # Relationships
    items = db.relationship('CartItem', backref='cart', lazy=True, cascade='all, delete-orphan')


class CartItem(db.Model):
    __tablename__ = 'cart_items'

    cart_item_id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('carts.cart_id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('menu_items.item_id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)

    # Relationships
    menu_item = db.relationship('MenuItem', backref='cart_items', lazy=True)


class Order(db.Model):
    __tablename__ = 'orders'

    order_id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    discount_amount = db.Column(db.Numeric(10, 2), default=0.00)
    order_status = db.Column(db.Enum('Placed', 'Confirmed', 'Preparing', 'Out for Delivery', 'Delivered', 'Cancelled'), default='Placed')
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.restaurant_id'), nullable=True)
    delivery_address = db.Column(db.Text)
    special_instructions = db.Column(db.Text)

    # Relationships
    order_items = db.relationship('OrderItem', backref='order', lazy=True)
    payment = db.relationship('Payment', backref='order', uselist=False, lazy=True)
    delivery = db.relationship('Delivery', backref='order', uselist=False, lazy=True)
    coupon_usage = db.relationship('OrderCoupon', backref='order', uselist=False, lazy=True)


class OrderItem(db.Model):
    __tablename__ = 'order_items'

    order_item_id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, default=1)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('menu_items.item_id'), nullable=False)

    # Relationships
    menu_item = db.relationship('MenuItem', backref='order_items', lazy=True)


class Payment(db.Model):
    __tablename__ = 'payments'

    payment_id = db.Column(db.Integer, primary_key=True)
    payment_mode = db.Column(db.Enum('UPI', 'Credit Card', 'Debit Card', 'Cash on Delivery'), nullable=False)
    payment_status = db.Column(db.Enum('Pending', 'Success', 'Failed', 'Refunded'), default='Pending')
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), unique=True, nullable=False)


class DeliveryPerson(db.Model):
    __tablename__ = 'delivery_persons'

    delivery_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    vehicle_type = db.Column(db.Enum('Bike', 'Scooter', 'Car', 'Bicycle'), default='Bike')
    status = db.Column(db.Enum('AVAILABLE', 'BUSY'), default='AVAILABLE')
    rating = db.Column(db.Numeric(2, 1), default=5.0)

    # Relationships
    deliveries = db.relationship('Delivery', backref='delivery_person', lazy=True)


class Delivery(db.Model):
    __tablename__ = 'deliveries'

    delivery_tracking_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), nullable=False)
    delivery_id = db.Column(db.Integer, db.ForeignKey('delivery_persons.delivery_id'), nullable=False)
    assigned_time = db.Column(db.DateTime, default=datetime.utcnow)
    picked_time = db.Column(db.DateTime)
    delivered_time = db.Column(db.DateTime)
    delivery_status = db.Column(db.Enum('ASSIGNED', 'PICKED', 'IN_TRANSIT', 'DELIVERED'), default='ASSIGNED')


class RestaurantReview(db.Model):
    __tablename__ = 'restaurant_reviews'

    review_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.restaurant_id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Coupon(db.Model):
    __tablename__ = 'coupons'

    coupon_id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    discount_percentage = db.Column(db.Numeric(5, 2), nullable=False)
    min_order_amount = db.Column(db.Numeric(10, 2), default=0.00)
    max_discount = db.Column(db.Numeric(10, 2), default=999.00)
    expiry_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.Enum('ACTIVE', 'EXPIRED'), default='ACTIVE')
    usage_limit = db.Column(db.Integer, default=100)
    times_used = db.Column(db.Integer, default=0)


class OrderCoupon(db.Model):
    __tablename__ = 'order_coupons'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), nullable=False)
    coupon_id = db.Column(db.Integer, db.ForeignKey('coupons.coupon_id'), nullable=False)

    coupon = db.relationship('Coupon', backref='usages', lazy=True)
