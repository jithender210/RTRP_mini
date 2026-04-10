from functools import wraps
import sqlite3
from flask import Flask, flash, redirect, render_template, request, session, url_for

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT UNIQUE,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()
app = Flask(__name__)
app.secret_key = "electronics-store-demo-secret"


PRODUCTS = [
    {
        "id": 1,
        "name": "NovaBook Air",
        "category": "Laptops",
        "price": 89999,
        "tag": "Best Seller",
        "description": "Thin, fast, and ready for work or play.",
    },
    {
        "id": 2,
        "name": "Pulse X Pro",
        "category": "Smartphones",
        "price": 64999,
        "tag": "New Launch",
        "description": "Flagship power with a stunning OLED display.",
    },
    {
        "id": 3,
        "name": "EchoBuds Max",
        "category": "Audio",
        "price": 9999,
        "tag": "Hot Deal",
        "description": "Immersive sound with all-day battery life.",
    },
    {
        "id": 4,
        "name": "VisionPad 11",
        "category": "Tablets",
        "price": 42999,
        "tag": "Top Rated",
        "description": "Portable productivity for creators and students.",
    },
    {
        "id": 5,
        "name": "Orbit Watch S",
        "category": "Wearables",
        "price": 14999,
        "tag": "Trending",
        "description": "Health tracking and smart controls on your wrist.",
    },
    {
        "id": 6,
        "name": "Volt Gaming Rig",
        "category": "Gaming",
        "price": 124999,
        "tag": "Premium",
        "description": "Desktop-class performance in a sleek build.",
    },
]


def format_currency(value):
    return f"Rs. {value:,.0f}"


app.jinja_env.filters["currency"] = format_currency


def get_product(product_id):
    return next((product for product in PRODUCTS if product["id"] == product_id), None)


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "user_email" not in session:
            flash("Please log in to continue.", "warning")
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapped_view


@app.context_processor
def inject_cart_count():
    cart = session.get("cart", {})
    count = sum(cart.values())
    return {"cart_count": count}


@app.route("/")
def index():
    if "user_email" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route('/register', methods=["GET","POST"])
def register():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        print(name, email, password)
        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            (name, email, password)
        )

        conn.commit()
        conn.close()

        return redirect(url_for('login'))

    return render_template('register.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "").strip()
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
        user = cursor.fetchone()
        if user:
            session["user_email"] = email
            session["cart"] = {}


            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Invalid email or password.")    

        flash("Invalid email or password.", "danger")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    featured_products = PRODUCTS[:4]
    categories = sorted({product["category"] for product in PRODUCTS})

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    user = cursor.execute(
        "SELECT * FROM users WHERE email = ?",
        (session["user_email"],)
    ).fetchone()
    
    conn.close()

    return render_template(
        "dashboard.html",
        featured_products=featured_products,
        categories=categories,
        user=user[1],
    )

@app.route("/categories")
@login_required
def categories():
    selected_category = request.args.get("category", "All")
    categories_list = ["All"] + sorted({product["category"] for product in PRODUCTS})

    if selected_category == "All":
        filtered_products = PRODUCTS
    else:
        filtered_products = [
            product for product in PRODUCTS if product["category"] == selected_category
        ]

    return render_template(
        "categories.html",
        products=filtered_products,
        categories=categories_list,
        selected_category=selected_category,
    )


@app.route("/cart")
@login_required
def cart():
    raw_cart = session.get("cart", {})
    cart_items = []
    subtotal = 0

    for product_id_str, quantity in raw_cart.items():
        product = get_product(int(product_id_str))
        if not product:
            continue

        line_total = product["price"] * quantity
        subtotal += line_total
        cart_items.append(
            {
                "product": product,
                "quantity": quantity,
                "line_total": line_total,
            }
        )

    shipping = 0 if subtotal > 50000 or subtotal == 0 else 499
    total = subtotal + shipping

    return render_template(
        "cart.html",
        cart_items=cart_items,
        subtotal=subtotal,
        shipping=shipping,
        total=total,
    )


@app.route("/add-to-cart/<int:product_id>", methods=["POST"])
@login_required
def add_to_cart(product_id):
    product = get_product(product_id)
    if not product:
        flash("Product not found.", "danger")
        return redirect(url_for("categories"))

    cart = session.get("cart", {})
    key = str(product_id)
    cart[key] = cart.get(key, 0) + 1
    session["cart"] = cart
    flash(f"{product['name']} added to cart.", "success")

    next_page = request.form.get("next_page", "categories")
    return redirect(url_for(next_page))


@app.route("/update-cart/<int:product_id>", methods=["POST"])
@login_required
def update_cart(product_id):
    quantity = int(request.form.get("quantity", 1))
    cart = session.get("cart", {})
    key = str(product_id)

    if quantity <= 0:
        cart.pop(key, None)
    else:
        cart[key] = quantity

    session["cart"] = cart
    flash("Cart updated.", "info")
    return redirect(url_for("cart"))


@app.route("/remove-from-cart/<int:product_id>", methods=["POST"])
@login_required
def remove_from_cart(product_id):
    cart = session.get("cart", {})
    cart.pop(str(product_id), None)
    session["cart"] = cart
    flash("Item removed from cart.", "info")
    return redirect(url_for("cart"))


if __name__ == "__main__":
    app.run(debug=True)
