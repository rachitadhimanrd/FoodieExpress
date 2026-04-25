from app import create_app, db
from app.models import Category, Restaurant, MenuItem, User
from werkzeug.security import generate_password_hash

def seed():
    app = create_app()
    with app.app_context():
        # Check if already seeded
        if Category.query.first():
            print("Database already seeded!")
            return

        # Categories
        cats = [
            Category(name='North Indian', icon='<i class="fas fa-pepper-hot"></i>'),
            Category(name='Chinese', icon='<i class="fas fa-bowl-rice"></i>'),
            Category(name='Italian', icon='<i class="fas fa-pizza-slice"></i>'),
            Category(name='Fast Food', icon='<i class="fas fa-hamburger"></i>'),
            Category(name='Beverages', icon='<i class="fas fa-glass-whiskey"></i>'),
            Category(name='Desserts', icon='<i class="fas fa-ice-cream"></i>')
        ]
        db.session.add_all(cats)
        db.session.commit()
        
        # Restaurants
        r1 = Restaurant(name='Punjabi Rasoi', cuisine_type='North Indian', rating=4.5, delivery_time='30-40 min', image_url='https://images.unsplash.com/photo-1585937421606-2b509f6b47cc?w=500&q=80', location='Sector 15, City')
        r2 = Restaurant(name='Pizza House', cuisine_type='Italian', rating=4.2, delivery_time='25-35 min', image_url='https://images.unsplash.com/photo-1513104890138-7c749659a591?w=500&q=80', location='Mall Road, City')
        r3 = Restaurant(name='Wok Express', cuisine_type='Chinese', rating=4.0, delivery_time='20-30 min', image_url='https://images.unsplash.com/photo-1552611052-33e04de081de?w=500&q=80', location='Central Market, City')
        r4 = Restaurant(name='Burger King', cuisine_type='Fast Food', rating=4.3, delivery_time='15-25 min', image_url='https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=500&q=80', location='Down Town, City')
        r5 = Restaurant(name='Healthy Bites', cuisine_type='Salads & Bowls', rating=4.6, delivery_time='30-45 min', image_url='https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=500&q=80', location='Green Park, City')
        r6 = Restaurant(name='Tandoori Nights', cuisine_type='North Indian', rating=4.4, delivery_time='35-50 min', image_url='https://images.unsplash.com/photo-1628294895950-9805252327bc?w=500&q=80', location='Old City, City')
        
        db.session.add_all([r1, r2, r3, r4, r5, r6])
        db.session.commit()

        # Admin User
        admin = User(name='Admin', email='admin@foodie.com', password_hash=generate_password_hash('admin123'), is_admin=True)
        db.session.add(admin)
        db.session.commit()

        # Menu Items
        items = [
            MenuItem(item_name='Paneer Tikka', price=249, category_id=1, restaurant_id=1, image_url='https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?w=500&q=80'),
            MenuItem(item_name='Butter Chicken', price=349, category_id=1, restaurant_id=1, image_url='https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?w=500&q=80'),
            MenuItem(item_name='Margherita Pizza', price=299, category_id=3, restaurant_id=2, image_url='https://images.unsplash.com/photo-1513104890138-7c749659a591?w=500&q=80'),
            MenuItem(item_name='Classic Chicken Burger', price=199, category_id=4, restaurant_id=4, image_url='https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=500&q=80'),
            MenuItem(item_name='Hakka Noodles', price=179, category_id=2, restaurant_id=3, image_url='https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=500&q=80'),
            MenuItem(item_name='Caesar Salad', price=229, category_id=5, restaurant_id=5, image_url='https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=500&q=80')
        ]
        db.session.add_all(items)
        db.session.commit()
        
        print("SQLite Database seeded successfully!")

if __name__ == '__main__':
    seed()
