import mysql.connector
import os

def create_database():
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST", "mysql-container"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "root123")
    )

    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS store_db")
    cursor.execute("USE store_db")

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(100),
            password VARCHAR(255)
        )
    """)

    # Products table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products(
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            price FLOAT
        )
    """)

    # Orders table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders(
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            product_name VARCHAR(100),
            price FLOAT
        )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()