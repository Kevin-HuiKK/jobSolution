import sqlite3
from datetime import datetime

def check_database():
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    
    print("\n=== 用户列表 ===")
    cursor.execute("SELECT id, username, email, name, is_admin FROM user")
    users = cursor.fetchall()
    for user in users:
        print(f"ID: {user[0]}")
        print(f"用户名: {user[1]}")
        print(f"邮箱: {user[2]}")
        print(f"姓名: {user[3]}")
        print(f"是否管理员: {user[4]}")
        print("-" * 30)
    
    print("\n=== 数据库表信息 ===")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    for table in tables:
        print(f"\n表名: {table[0]}")
        cursor.execute(f"PRAGMA table_info({table[0]})")
        columns = cursor.fetchall()
        print("列信息:")
        for col in columns:
            print(f"  {col[1]} ({col[2]})")
    
    conn.close()

if __name__ == '__main__':
    check_database() 