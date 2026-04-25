import pymysql
import os

images = {
    'pizza': 'https://images.unsplash.com/photo-1513104890138-7c749659a591?w=500&q=80',
    'burger': 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=500&q=80',
    'pasta': 'https://images.unsplash.com/photo-1621996316562-b91c0e352ab9?w=500&q=80',
    'kebab': 'https://images.unsplash.com/photo-1603360946369-dc9bb6258143?w=500&q=80',
    'tikka': 'https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?w=500&q=80',
    'paneer': 'https://images.unsplash.com/photo-1631452180519-c014fe946bc0?w=500&q=80',
    'dal': 'https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=500&q=80',
    'naan': 'https://images.unsplash.com/photo-1601050690597-df0568f70950?w=500&q=80',
    'biryani': 'https://images.unsplash.com/photo-1589302168068-964664d93cb0?w=500&q=80',
    'wrap': 'https://images.unsplash.com/photo-1626700051175-6818013e1d4f?w=500&q=80',
    'salad': 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=500&q=80',
    'soup': 'https://images.unsplash.com/photo-1547592180-85f173990554?w=500&q=80',
    'sushi': 'https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=500&q=80',
    'noodles': 'https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=500&q=80',
    'dessert': 'https://images.unsplash.com/photo-1563805042-7684c8a9e9ce?w=500&q=80',
    'cake': 'https://images.unsplash.com/photo-1578985545062-69928b1ea388?w=500&q=80',
    'brownie': 'https://images.unsplash.com/photo-1606313564200-e75d5e30476c?w=500&q=80',
    'default': 'https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=500&q=80'
}

def update_images():
    conn = pymysql.connect(host='localhost', user='root', password='rachita', database='food_ordering_db')
    cursor = conn.cursor()
    cursor.execute("SELECT item_id, item_name FROM menu_items")
    items = cursor.fetchall()
    
    for item in items:
        item_id = item[0]
        item_name = item[1].lower()
        img_url = images['default']
        
        for key, url in images.items():
            if key in item_name and key != 'default':
                img_url = url
                break
                
        cursor.execute("UPDATE menu_items SET image_url = %s WHERE item_id = %s", (img_url, item_id))
        
    conn.commit()
    conn.close()
    print("Updated menu item images successfully!")

if __name__ == '__main__':
    update_images()
