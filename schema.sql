-- =============================================
-- Online Food Ordering System — Full Schema
-- MySQL 9.6 Compatible
-- =============================================

CREATE DATABASE IF NOT EXISTS food_ordering_db;
USE food_ordering_db;

-- =============================================
-- 1. USERS
-- =============================================
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    phone VARCHAR(20),
    address TEXT,
    password_hash VARCHAR(255) NOT NULL,
    is_admin TINYINT(1) DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- =============================================
-- 2. RESTAURANTS
-- =============================================
CREATE TABLE IF NOT EXISTS restaurants (
    restaurant_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    location VARCHAR(255) NOT NULL,
    rating DECIMAL(2,1) DEFAULT 0.0,
    description TEXT,
    image_url VARCHAR(500),
    cuisine_type VARCHAR(100),
    delivery_time VARCHAR(50) DEFAULT '30-45 min',
    is_active TINYINT(1) DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- =============================================
-- 3. CATEGORIES
-- =============================================
CREATE TABLE IF NOT EXISTS categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    icon VARCHAR(50) DEFAULT '🍽️'
) ENGINE=InnoDB;

-- =============================================
-- 4. MENU ITEMS
-- =============================================
CREATE TABLE IF NOT EXISTS menu_items (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(150) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    description TEXT,
    image_url VARCHAR(500),
    is_available TINYINT(1) DEFAULT 1,
    restaurant_id INT NOT NULL,
    category_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(category_id) ON DELETE RESTRICT,
    INDEX idx_menu_restaurant (restaurant_id),
    INDEX idx_menu_category (category_id)
) ENGINE=InnoDB;

-- =============================================
-- 5. CARTS
-- =============================================
CREATE TABLE IF NOT EXISTS carts (
    cart_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    status ENUM('ACTIVE', 'ORDERED') DEFAULT 'ACTIVE',
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_cart_user (user_id)
) ENGINE=InnoDB;

-- =============================================
-- 6. CART ITEMS
-- =============================================
CREATE TABLE IF NOT EXISTS cart_items (
    cart_item_id INT AUTO_INCREMENT PRIMARY KEY,
    cart_id INT NOT NULL,
    item_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    FOREIGN KEY (cart_id) REFERENCES carts(cart_id) ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES menu_items(item_id) ON DELETE CASCADE,
    UNIQUE KEY uk_cart_item (cart_id, item_id)
) ENGINE=InnoDB;

-- =============================================
-- 7. ORDERS
-- =============================================
CREATE TABLE IF NOT EXISTS orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10,2) NOT NULL,
    discount_amount DECIMAL(10,2) DEFAULT 0.00,
    order_status ENUM('Placed', 'Confirmed', 'Preparing', 'Out for Delivery', 'Delivered', 'Cancelled') DEFAULT 'Placed',
    user_id INT NOT NULL,
    restaurant_id INT NOT NULL,
    delivery_address TEXT,
    special_instructions TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id) ON DELETE CASCADE,
    INDEX idx_order_user (user_id),
    INDEX idx_order_restaurant (restaurant_id),
    INDEX idx_order_status (order_status)
) ENGINE=InnoDB;

-- =============================================
-- 8. ORDER ITEMS
-- =============================================
CREATE TABLE IF NOT EXISTS order_items (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    quantity INT NOT NULL DEFAULT 1,
    price DECIMAL(10,2) NOT NULL,
    order_id INT NOT NULL,
    item_id INT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES menu_items(item_id) ON DELETE CASCADE,
    INDEX idx_oi_order (order_id)
) ENGINE=InnoDB;

-- =============================================
-- 9. PAYMENTS
-- =============================================
CREATE TABLE IF NOT EXISTS payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    payment_mode ENUM('UPI', 'Credit Card', 'Debit Card', 'Cash on Delivery') NOT NULL,
    payment_status ENUM('Pending', 'Success', 'Failed', 'Refunded') DEFAULT 'Pending',
    payment_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    amount DECIMAL(10,2) NOT NULL,
    order_id INT NOT NULL UNIQUE,
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- =============================================
-- 10. DELIVERY PERSONS
-- =============================================
CREATE TABLE IF NOT EXISTS delivery_persons (
    delivery_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    vehicle_type ENUM('Bike', 'Scooter', 'Car', 'Bicycle') DEFAULT 'Bike',
    status ENUM('AVAILABLE', 'BUSY') DEFAULT 'AVAILABLE',
    rating DECIMAL(2,1) DEFAULT 5.0
) ENGINE=InnoDB;

-- =============================================
-- 11. DELIVERIES (Order Tracking)
-- =============================================
CREATE TABLE IF NOT EXISTS deliveries (
    delivery_tracking_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    delivery_id INT NOT NULL,
    assigned_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    picked_time DATETIME,
    delivered_time DATETIME,
    delivery_status ENUM('ASSIGNED', 'PICKED', 'IN_TRANSIT', 'DELIVERED') DEFAULT 'ASSIGNED',
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (delivery_id) REFERENCES delivery_persons(delivery_id) ON DELETE CASCADE,
    INDEX idx_delivery_order (order_id)
) ENGINE=InnoDB;

-- =============================================
-- 12. RESTAURANT REVIEWS
-- =============================================
CREATE TABLE IF NOT EXISTS restaurant_reviews (
    review_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    restaurant_id INT NOT NULL,
    rating INT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    comment TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id) ON DELETE CASCADE,
    INDEX idx_review_restaurant (restaurant_id)
) ENGINE=InnoDB;

-- =============================================
-- 13. COUPONS
-- =============================================
CREATE TABLE IF NOT EXISTS coupons (
    coupon_id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50) NOT NULL UNIQUE,
    discount_percentage DECIMAL(5,2) NOT NULL,
    min_order_amount DECIMAL(10,2) DEFAULT 0.00,
    max_discount DECIMAL(10,2) DEFAULT 999.00,
    expiry_date DATE NOT NULL,
    status ENUM('ACTIVE', 'EXPIRED') DEFAULT 'ACTIVE',
    usage_limit INT DEFAULT 100,
    times_used INT DEFAULT 0
) ENGINE=InnoDB;

-- =============================================
-- 14. ORDER COUPONS
-- =============================================
CREATE TABLE IF NOT EXISTS order_coupons (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    coupon_id INT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (coupon_id) REFERENCES coupons(coupon_id) ON DELETE CASCADE,
    UNIQUE KEY uk_order_coupon (order_id)
) ENGINE=InnoDB;


-- =============================================
-- SEED DATA
-- =============================================

-- Admin user (password: admin123)
INSERT INTO users (name, email, phone, address, password_hash, is_admin) VALUES
('Admin', 'admin@foodie.com', '9999999999', 'System', 'scrypt:32768:8:1$salt$admin_hash_placeholder', 1);

-- Regular users (password: pass123)
INSERT INTO users (name, email, phone, address, password_hash) VALUES
('Rahul Sharma', 'rahul@gmail.com', '9876543210', '12 MG Road, Bangalore', 'placeholder'),
('Priya Patel', 'priya@gmail.com', '9876543211', '45 Park Street, Mumbai', 'placeholder'),
('Amit Kumar', 'amit@gmail.com', '9876543212', '78 Connaught Place, Delhi', 'placeholder');

-- Restaurants
INSERT INTO restaurants (name, location, rating, description, image_url, cuisine_type, delivery_time) VALUES
('The Spice Garden', 'Koramangala, Bangalore', 4.5, 'Authentic Indian cuisine with a modern twist. Our chefs bring you the finest flavors from across India.', '/static/images/rest1.jpg', 'Indian', '25-35 min'),
('Pizza Paradise', 'Indiranagar, Bangalore', 4.2, 'Wood-fired pizzas made with imported Italian ingredients. Crispy crusts and generous toppings.', '/static/images/rest2.jpg', 'Italian', '30-40 min'),
('Dragon Wok', 'HSR Layout, Bangalore', 4.3, 'Experience authentic Chinese and Pan-Asian flavors. Fresh ingredients, bold tastes.', '/static/images/rest3.jpg', 'Chinese', '20-30 min'),
('Burger Barn', 'Whitefield, Bangalore', 4.1, 'Juicy handcrafted burgers with premium beef and chicken patties. Sides that complete the meal.', '/static/images/rest4.jpg', 'American', '20-25 min'),
('Green Bowl', 'JP Nagar, Bangalore', 4.6, 'Healthy, delicious salads and bowls made with organic, locally-sourced ingredients.', '/static/images/rest5.jpg', 'Healthy', '15-25 min'),
('Tandoori Nights', 'MG Road, Bangalore', 4.4, 'Premium tandoori and North Indian cuisine. Kebabs, curries, and biryanis to die for.', '/static/images/rest6.jpg', 'Indian', '30-45 min');

-- Categories
INSERT INTO categories (category_id, name, description, icon) VALUES
(1, 'Starters', 'Appetizers and snacks to begin your meal', '🥗'),
(2, 'Main Course', 'Hearty main dishes and entrées', '🍛'),
(3, 'Pizza', 'Hand-tossed and wood-fired pizzas', '🍕'),
(4, 'Burgers', 'Juicy burgers with premium ingredients', '🍔'),
(5, 'Desserts', 'Sweet treats to end your meal', '🍰'),
(6, 'Beverages', 'Refreshing drinks and beverages', '🥤'),
(7, 'Biryani', 'Aromatic rice dishes with meats and spices', '🍚'),
(8, 'Chinese', 'Noodles, rice, and stir-fry dishes', '🥡'),
(9, 'Healthy', 'Salads, bowls, and nutritious options', '🥬');

-- Menu Items — The Spice Garden (restaurant_id=1)
INSERT INTO menu_items (item_name, price, description, image_url, restaurant_id, category_id) VALUES
('Paneer Tikka', 249.00, 'Marinated cottage cheese cubes grilled to perfection in tandoor', '/static/images/food/paneer_tikka.jpg', 1, 1),
('Chicken 65', 299.00, 'Spicy deep-fried chicken with curry leaves and red chillies', '/static/images/food/chicken_65.jpg', 1, 1),
('Butter Chicken', 349.00, 'Tender chicken in rich, creamy tomato gravy', '/static/images/food/butter_chicken.jpg', 1, 2),
('Dal Makhani', 249.00, 'Slow-cooked black lentils in a buttery, creamy sauce', '/static/images/food/dal_makhani.jpg', 1, 2),
('Hyderabadi Biryani', 399.00, 'Fragrant basmati rice layered with spiced chicken and herbs', '/static/images/food/biryani.jpg', 1, 7),
('Gulab Jamun', 149.00, 'Soft milk-solid dumplings soaked in rose-flavored sugar syrup', '/static/images/food/gulab_jamun.jpg', 1, 5),
('Mango Lassi', 129.00, 'Creamy yogurt smoothie blended with fresh alphonso mangoes', '/static/images/food/mango_lassi.jpg', 1, 6);

-- Menu Items — Pizza Paradise (restaurant_id=2)
INSERT INTO menu_items (item_name, price, description, image_url, restaurant_id, category_id) VALUES
('Garlic Bread', 179.00, 'Crispy baguette with garlic butter and herbs', '/static/images/food/garlic_bread.jpg', 2, 1),
('Margherita Pizza', 349.00, 'Classic pizza with fresh mozzarella, tomato sauce, and basil', '/static/images/food/margherita.jpg', 2, 3),
('Pepperoni Pizza', 449.00, 'Loaded with spicy pepperoni and melted mozzarella cheese', '/static/images/food/pepperoni.jpg', 2, 3),
('BBQ Chicken Pizza', 499.00, 'Smoky BBQ sauce, grilled chicken, onions, and bell peppers', '/static/images/food/bbq_pizza.jpg', 2, 3),
('Farmhouse Pizza', 399.00, 'Fresh vegetables, olives, and mushrooms on a crispy crust', '/static/images/food/farmhouse.jpg', 2, 3),
('Tiramisu', 249.00, 'Classic Italian coffee-flavored layered dessert', '/static/images/food/tiramisu.jpg', 2, 5),
('Cold Coffee', 149.00, 'Chilled coffee blended with ice cream and chocolate', '/static/images/food/cold_coffee.jpg', 2, 6);

-- Menu Items — Dragon Wok (restaurant_id=3)
INSERT INTO menu_items (item_name, price, description, image_url, restaurant_id, category_id) VALUES
('Spring Rolls', 199.00, 'Crispy rolls stuffed with vegetables and glass noodles', '/static/images/food/spring_rolls.jpg', 3, 1),
('Manchurian', 249.00, 'Crispy veggie balls in tangy, spicy Manchurian sauce', '/static/images/food/manchurian.jpg', 3, 8),
('Hakka Noodles', 279.00, 'Stir-fried noodles with vegetables and soy sauce', '/static/images/food/hakka_noodles.jpg', 3, 8),
('Schezwan Fried Rice', 269.00, 'Spicy fried rice with Schezwan sauce and veggies', '/static/images/food/schezwan_rice.jpg', 3, 8),
('Chilli Chicken', 329.00, 'Crispy chicken tossed in spicy chilli sauce', '/static/images/food/chilli_chicken.jpg', 3, 8),
('Ice Cream Sundae', 179.00, 'Vanilla ice cream with chocolate sauce and nuts', '/static/images/food/sundae.jpg', 3, 5);

-- Menu Items — Burger Barn (restaurant_id=4)
INSERT INTO menu_items (item_name, price, description, image_url, restaurant_id, category_id) VALUES
('Classic Chicken Burger', 249.00, 'Juicy chicken patty with lettuce, tomato, and special sauce', '/static/images/food/chicken_burger.jpg', 4, 4),
('Double Cheese Burger', 349.00, 'Two beef patties with double cheddar and caramelized onions', '/static/images/food/cheese_burger.jpg', 4, 4),
('Veggie Burger', 229.00, 'Crispy veggie patty with avocado and ranch dressing', '/static/images/food/veggie_burger.jpg', 4, 4),
('Loaded Fries', 199.00, 'Crispy fries topped with cheese, bacon, and jalapeños', '/static/images/food/loaded_fries.jpg', 4, 1),
('Chocolate Shake', 179.00, 'Thick and creamy chocolate milkshake', '/static/images/food/choc_shake.jpg', 4, 6);

-- Menu Items — Green Bowl (restaurant_id=5)
INSERT INTO menu_items (item_name, price, description, image_url, restaurant_id, category_id) VALUES
('Caesar Salad', 299.00, 'Crisp romaine, parmesan, croutons with Caesar dressing', '/static/images/food/caesar_salad.jpg', 5, 9),
('Quinoa Bowl', 349.00, 'Protein-rich quinoa with roasted vegetables and tahini', '/static/images/food/quinoa_bowl.jpg', 5, 9),
('Avocado Toast', 279.00, 'Sourdough toast with smashed avocado, seeds, and microgreens', '/static/images/food/avocado_toast.jpg', 5, 9),
('Smoothie Bowl', 249.00, 'Açaí base topped with granola, berries, and coconut', '/static/images/food/smoothie_bowl.jpg', 5, 9),
('Green Detox Juice', 199.00, 'Fresh spinach, apple, ginger, and lemon juice', '/static/images/food/green_juice.jpg', 5, 6);

-- Menu Items — Tandoori Nights (restaurant_id=6)
INSERT INTO menu_items (item_name, price, description, image_url, restaurant_id, category_id) VALUES
('Seekh Kebab', 329.00, 'Minced lamb kebabs with aromatic spices, grilled on skewers', '/static/images/food/seekh_kebab.jpg', 6, 1),
('Chicken Tikka', 299.00, 'Boneless chicken marinated in yogurt and spices, chargrilled', '/static/images/food/chicken_tikka.jpg', 6, 1),
('Mutton Rogan Josh', 449.00, 'Slow-cooked Kashmiri-style mutton in rich red curry', '/static/images/food/rogan_josh.jpg', 6, 2),
('Veg Biryani', 299.00, 'Fragrant basmati rice with mixed vegetables and whole spices', '/static/images/food/veg_biryani.jpg', 6, 7),
('Chicken Biryani', 399.00, 'Aromatic dum biryani with tender chicken pieces', '/static/images/food/chicken_biryani.jpg', 6, 7),
('Phirni', 149.00, 'Traditional ground rice pudding with cardamom and saffron', '/static/images/food/phirni.jpg', 6, 5);

-- Delivery Persons
INSERT INTO delivery_persons (name, phone, vehicle_type, status) VALUES
('Ravi Kumar', '9000000001', 'Bike', 'AVAILABLE'),
('Suresh M', '9000000002', 'Scooter', 'AVAILABLE'),
('Deepak R', '9000000003', 'Bike', 'AVAILABLE'),
('Karthik S', '9000000004', 'Bicycle', 'AVAILABLE'),
('Manoj P', '9000000005', 'Car', 'AVAILABLE');

-- Coupons
INSERT INTO coupons (code, discount_percentage, min_order_amount, max_discount, expiry_date, status) VALUES
('WELCOME50', 50.00, 200.00, 150.00, '2027-12-31', 'ACTIVE'),
('SAVE20', 20.00, 300.00, 100.00, '2027-06-30', 'ACTIVE'),
('FLAT10', 10.00, 100.00, 50.00, '2027-12-31', 'ACTIVE'),
('FOODIE30', 30.00, 500.00, 200.00, '2027-03-31', 'ACTIVE'),
('NEWUSER', 40.00, 150.00, 120.00, '2027-12-31', 'ACTIVE');
