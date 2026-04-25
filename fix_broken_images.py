import pymysql

broken_images = {
    30: 'https://images.unsplash.com/photo-1600271886742-f049cd451bba?w=500&q=80', # Green Detox Juice (Orange Juice)
    33: 'https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=500&q=80', # Mutton Rogan Josh (Curry)
    35: 'https://images.unsplash.com/photo-1631515243349-e0cb75fb8d3a?w=500&q=80', # Chicken Biryani
    36: 'https://images.unsplash.com/photo-1551024601-bec78aea704b?w=500&q=80', # Phirni (Dessert)
    15: 'https://images.unsplash.com/photo-1594974377017-d2b51ccdf748?w=500&q=80', # Spring Rolls
    20: 'https://images.unsplash.com/photo-1557142046-c704a3adf364?w=500&q=80', # Ice Cream Sundae
    8:  'https://images.unsplash.com/photo-1619535860434-ba1d8fa12536?w=500&q=80', # Garlic Bread
    10: 'https://images.unsplash.com/photo-1628840042765-356cda07504e?w=500&q=80', # Pepperoni Pizza
    13: 'https://images.unsplash.com/photo-1587314168485-3236d6710814?w=500&q=80', # Tiramisu (Cake)
    24: 'https://images.unsplash.com/photo-1585692277358-e3668f44ff53?w=500&q=80', # Loaded Fries
    6:  'https://images.unsplash.com/photo-1551024506-0bccd828d307?w=500&q=80', # Gulab Jamun (Dessert)
    7:  'https://images.unsplash.com/photo-1544145945-f90425340c7e?w=500&q=80'  # Mango Lassi (Drink)
}

def update_images():
    conn = pymysql.connect(host='localhost', user='root', password='rachita', database='food_ordering_db')
    cursor = conn.cursor()
    
    for item_id, url in broken_images.items():
        cursor.execute("UPDATE menu_items SET image_url = %s WHERE item_id = %s", (url, item_id))
        
    conn.commit()
    conn.close()
    print("Fixed broken images successfully!")

if __name__ == '__main__':
    update_images()
