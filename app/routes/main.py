from flask import Blueprint, render_template, request
from app.models import Restaurant, MenuItem, Category, RestaurantReview
from sqlalchemy import func

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def home():
    restaurants = Restaurant.query.filter_by(is_active=True).order_by(Restaurant.rating.desc()).limit(6).all()
    categories = Category.query.all()
    
    locations = Restaurant.query.with_entities(Restaurant.location).distinct().all()
    areas = list(set([loc[0].split(',')[0].strip() for loc in locations if loc[0]]))
    areas.sort()
    
    return render_template('home.html', restaurants=restaurants, categories=categories, areas=areas)


@main_bp.route('/restaurants')
def restaurants():
    search = request.args.get('search', '').strip()
    category_filter = request.args.get('category', '').strip()
    area_filter = request.args.get('area', '').strip()

    query = Restaurant.query.filter_by(is_active=True)

    if search:
        query = query.filter(
            (Restaurant.name.ilike(f'%{search}%')) |
            (Restaurant.cuisine_type.ilike(f'%{search}%')) |
            (Restaurant.location.ilike(f'%{search}%'))
        )

    if category_filter:
        # Filter restaurants that have items in this category
        query = query.filter(
            Restaurant.menu_items.any(
                MenuItem.category.has(Category.name == category_filter)
            )
        )
        
    if area_filter:
        query = query.filter(Restaurant.location.ilike(f'%{area_filter}%'))

    restaurants = query.order_by(Restaurant.rating.desc()).all()
    categories = Category.query.all()
    
    locations = Restaurant.query.with_entities(Restaurant.location).distinct().all()
    areas = list(set([loc[0].split(',')[0].strip() for loc in locations if loc[0]]))
    areas.sort()

    return render_template(
        'restaurants/list.html',
        restaurants=restaurants,
        categories=categories,
        search=search,
        category_filter=category_filter,
        area_filter=area_filter,
        areas=areas
    )


@main_bp.route('/restaurant/<int:restaurant_id>/menu')
def restaurant_menu(restaurant_id):
    restaurant = Restaurant.query.get_or_404(restaurant_id)
    category_filter = request.args.get('category', '')

    query = MenuItem.query.filter_by(restaurant_id=restaurant_id, is_available=True)

    if category_filter:
        query = query.filter(MenuItem.category.has(Category.name == category_filter))

    menu_items = query.all()

    # Group items by category
    categories_with_items = {}
    for item in menu_items:
        cat_name = item.category.name
        if cat_name not in categories_with_items:
            categories_with_items[cat_name] = {
                'icon': item.category.icon,
                'items': []
            }
        categories_with_items[cat_name]['items'].append(item)

    # Get all categories for this restaurant
    restaurant_categories = Category.query.join(MenuItem).filter(
        MenuItem.restaurant_id == restaurant_id,
        MenuItem.is_available == True
    ).distinct().all()

    # Reviews
    reviews = RestaurantReview.query.filter_by(restaurant_id=restaurant_id)\
        .order_by(RestaurantReview.created_at.desc()).limit(10).all()

    avg_rating = RestaurantReview.query.filter_by(restaurant_id=restaurant_id)\
        .with_entities(func.avg(RestaurantReview.rating)).scalar()

    return render_template(
        'restaurants/menu.html',
        restaurant=restaurant,
        categories_with_items=categories_with_items,
        restaurant_categories=restaurant_categories,
        reviews=reviews,
        avg_rating=round(float(avg_rating), 1) if avg_rating else float(restaurant.rating),
        category_filter=category_filter
    )
