from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.cart import cart_bp
    from app.routes.orders import orders_bp
    from app.routes.payments import payments_bp
    from app.routes.reviews import reviews_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(payments_bp)
    app.register_blueprint(reviews_bp)
    app.register_blueprint(admin_bp)

    # Context processor for cart count
    @app.context_processor
    def inject_cart_count():
        from flask_login import current_user
        if current_user.is_authenticated:
            from app.models import Cart, CartItem
            cart = Cart.query.filter_by(user_id=current_user.user_id, status='ACTIVE').first()
            if cart:
                count = CartItem.query.filter_by(cart_id=cart.cart_id).count()
                return {'cart_count': count}
        return {'cart_count': 0}

    return app
