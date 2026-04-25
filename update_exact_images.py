import pymysql

images = {
    1: 'https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?w=500&q=80',
    2: 'https://images.unsplash.com/photo-1604908176997-125f25cc6f3d?w=500&q=80',
    3: 'https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?w=500&q=80',
    4: 'https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=500&q=80',
    5: 'https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=500&q=80',
    6: 'https://images.unsplash.com/photo-1563805042-7684c8a9e9ce?w=500&q=80',
    7: 'https://images.unsplash.com/photo-1556881286-fc6915169721?w=500&q=80',
    8: 'https://images.unsplash.com/photo-1573140247632-f8fd74997d5c?w=500&q=80',
    9: 'https://images.unsplash.com/photo-1513104890138-7c749659a591?w=500&q=80',
    10: 'https://images.unsplash.com/photo-1534308983496-4fabb1a015ce?w=500&q=80',
    11: 'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=500&q=80',
    12: 'https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=500&q=80',
    13: 'https://images.unsplash.com/photo-1571115177098-24c4281fba05?w=500&q=80',
    14: 'https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=500&q=80',
    15: 'https://images.unsplash.com/photo-1544025162-811c793ff6c4?w=500&q=80',
    16: 'https://images.unsplash.com/photo-1585032226651-759b368d7246?w=500&q=80',
    17: 'https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=500&q=80',
    18: 'https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=500&q=80',
    19: 'https://images.unsplash.com/photo-1604908176997-125f25cc6f3d?w=500&q=80',
    20: 'https://images.unsplash.com/photo-1563805042-7684c8a9e9ce?w=500&q=80',
    21: 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=500&q=80',
    22: 'https://images.unsplash.com/photo-1586816001966-79b736744398?w=500&q=80',
    23: 'https://images.unsplash.com/photo-1520072959219-c595dc870360?w=500&q=80',
    24: 'https://images.unsplash.com/photo-1576107232684-1279f3908594?w=500&q=80',
    25: 'https://images.unsplash.com/photo-1572490122747-3968b75cc699?w=500&q=80',
    26: 'https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=500&q=80',
    27: 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=500&q=80',
    28: 'https://images.unsplash.com/photo-1541519227354-08fa5d50c44d?w=500&q=80',
    29: 'https://images.unsplash.com/photo-1494597564530-871f2b93ac55?w=500&q=80',
    30: 'https://images.unsplash.com/photo-1622597467836-f38240662f40?w=500&q=80',
    31: 'https://images.unsplash.com/photo-1603360946369-dc9bb6258143?w=500&q=80',
    32: 'https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?w=500&q=80',
    33: 'https://images.unsplash.com/photo-1585937421606-2b509f6b47cc?w=500&q=80',
    34: 'https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=500&q=80',
    35: 'https://images.unsplash.com/photo-1589302168068-964664d93cb0?w=500&q=80',
    36: 'https://images.unsplash.com/photo-1563805042-7684c8a9e9ce?w=500&q=80'
}

def update_images():
    conn = pymysql.connect(host='localhost', user='root', password='rachita', database='food_ordering_db')
    cursor = conn.cursor()
    
    for item_id, url in images.items():
        cursor.execute("UPDATE menu_items SET image_url = %s WHERE item_id = %s", (url, item_id))
        
    conn.commit()
    conn.close()
    print("Exact images mapped to all 36 items!")

if __name__ == '__main__':
    update_images()
