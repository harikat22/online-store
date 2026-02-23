from flask import Flask, render_template, request, redirect, session
import mysql.connector
import bcrypt
import os
from db import create_database

app = Flask(__name__)
app.secret_key = "secretkey"

create_database()

def get_db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "mysql-container"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "root123"),
        database="store_db"
    )

# ---------------- REGISTER ----------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = bcrypt.hashpw(request.form['password'].encode(), bcrypt.gensalt())

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        conn.close()

        return redirect('/login')

    return render_template("register.html")

# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode()

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and bcrypt.checkpw(password, user[2].encode()):
            session['user_id'] = user[0]
            return redirect('/products')

    return render_template("login.html")

# ---------------- PRODUCTS ----------------
@app.route('/products')
def products():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()

    return render_template("products.html", products=products)

# ---------------- ADD TO CART ----------------
@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE id=%s", (product_id,))
    product = cursor.fetchone()
    conn.close()

    if 'cart' not in session:
        session['cart'] = []

    session['cart'].append(product)
    session.modified = True

    return redirect('/cart')

# ---------------- CART ----------------
@app.route('/cart')
def cart():
    cart = session.get('cart', [])
    return render_template("cart.html", cart=cart)

# ---------------- CHECKOUT ----------------
@app.route('/checkout')
def checkout():
    conn = get_db()
    cursor = conn.cursor()

    for item in session.get('cart', []):
        cursor.execute(
            "INSERT INTO orders (user_id, product_name, price) VALUES (%s, %s, %s)",
            (session['user_id'], item[1], item[2])
        )

    conn.commit()
    conn.close()

    session['cart'] = []
    return redirect('/orders')

# ---------------- ORDER HISTORY ----------------
@app.route('/orders')
def orders():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT product_name, price FROM orders WHERE user_id=%s", (session['user_id'],))
    orders = cursor.fetchall()
    conn.close()

    return render_template("orders.html", orders=orders)

# ---------------- ADMIN ADD PRODUCT ----------------
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO products (name, price) VALUES (%s, %s)", (name, price))
        conn.commit()
        conn.close()

    return render_template("admin.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)