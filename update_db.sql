USE food_ordering_db;
ALTER TABLE orders MODIFY restaurant_id INT NULL;

UPDATE categories SET icon='<i class="fas fa-utensils"></i>' WHERE name='Starters';
UPDATE categories SET icon='<i class="fas fa-drumstick-bite"></i>' WHERE name='Main Course';
UPDATE categories SET icon='<i class="fas fa-pizza-slice"></i>' WHERE name='Pizza';
UPDATE categories SET icon='<i class="fas fa-hamburger"></i>' WHERE name='Burgers';
UPDATE categories SET icon='<i class="fas fa-ice-cream"></i>' WHERE name='Desserts';
UPDATE categories SET icon='<i class="fas fa-glass-cheers"></i>' WHERE name='Beverages';
UPDATE categories SET icon='<i class="fas fa-bowl-rice"></i>' WHERE name='Biryani';
UPDATE categories SET icon='<i class="fas fa-pepper-hot"></i>' WHERE name='Chinese';
UPDATE categories SET icon='<i class="fas fa-leaf"></i>' WHERE name='Healthy';

UPDATE restaurants SET image_url='https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=500&q=80' WHERE restaurant_id=1;
UPDATE restaurants SET image_url='https://images.unsplash.com/photo-1552566626-52f8b828add9?w=500&q=80' WHERE restaurant_id=2;
UPDATE restaurants SET image_url='https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=500&q=80' WHERE restaurant_id=3;
UPDATE restaurants SET image_url='https://images.unsplash.com/photo-1544148103-0773bf10d330?w=500&q=80' WHERE restaurant_id=4;
UPDATE restaurants SET image_url='https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=500&q=80' WHERE restaurant_id=5;
UPDATE restaurants SET image_url='https://images.unsplash.com/photo-1466978913421-bac2e5e75b4e?w=500&q=80' WHERE restaurant_id=6;

UPDATE menu_items SET image_url='https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=500&q=80';
