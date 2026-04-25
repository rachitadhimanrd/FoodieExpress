import pymysql
import os
import re

def test_conn():
    with open('config.py', 'r') as f:
        content = f.read()
    
    match = re.search(r"or '(mysql\+pymysql://[^']+)'", content)
    if not match:
        print("Could not find connection string in config.py")
        return
    
    uri = match.group(1)
    print(f"Found URI: {uri[:20]}...")
    
    # Simple parse
    # mysql+pymysql://user:pass@host:port/db
    uri = uri.replace('mysql+pymysql://', '')
    user_pass, host_port_db = uri.split('@')
    user, password = user_pass.split(':')
    host_port, db = host_port_db.split('/')
    host, port = host_port.split(':')
    
    try:
        conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            port=int(port),
            database=db,
            connect_timeout=10
        )
        print("SUCCESS: Connected to Aiven!")
        conn.close()
    except Exception as e:
        print(f"FAILED: {e}")

if __name__ == '__main__':
    test_conn()
