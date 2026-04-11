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
        "name": "Boat airdopes 300",
        "category": "Audio",
        "Brand": "boat",
        "price": 1099,
        "tag": "Best Seller",
        "img_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTJ5UVHXQw8Lr5krVCLSvu6Lr0cuwRGVPsY5A&s",
        "description": "Boat Airdopes 300, Cinematic Spatial Audio, 50HRS Battery, 4Mic AI ENx, Fast Charge, App Support, Low Latency, IPX4, v5.3 Bluetooth Earbuds, TWS Ear Buds Wireless Earphones with mic (Gunmetal Black)."
    },
    {
        "id": 2,
        "name": "Tribit XSound Go Wireless Bluetooth ",
        "category": "Audio",
        "Brand": "Tribit",
        "price": 2843,
        "tag":"New Launch",
        "img_url":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSJBFjKVaIM69-xWVDguu3bEk7IR9gQ50SrDA&s",
        "description": "Tribit Updated Version XSound Go Wireless Bluetooth 5.3 Speakers with Loud Stereo Sound & Rich Bass 16W,24H Playtime,150 ft Bluetooth Range,Outdoor Lightweight IPX7 Waterproof,Built-in Mic (Black)"
    },
    {
        "id": 3,
        "name": "boAt Rockerz 480",
        "category": "Audio",
        "Brand":"boat",
        "price":1599 ,
        "tag":"Hot Deal",
        "img_url":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSldl-0EEgC2zcQLgUEfc8ldifBUkOPLoekHw&s",
        "description": "boAt Rockerz 480, RGB LEDs,6 Light Modes, 40mm Drivers,Beast Mode, 60H Battery, ENx Tech, Stream Ad Free Music via App Support, Bluetooth Headphones, Wireless Over Ear Headphone with Mic (Black Sabre)"
    },
    {
        "id": 4,
        "name": "JBL Partybox 320",
        "category": "Audio",
         "Brand":"JBL",
        "price":44999 ,
        "tag":"Top Deal",
        "img_url":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRE1gk-x9xNwY4dz16VwVSxcE13_fVx71RnIQ&s",
        "description":"Connectivity Technology=Bluetooth ,Speaker Maximum Output Power=240 Watts,Frequency Response=40 Hz,Audio Output Mode=Stereo",
        "About":"( Replacement, Installation & On-Site Repair within 24 hours( in Select cities). Powerful JBL Pro Sound Rock out with powerful JBL Pro Sound from two 6.5” woofers that deliver clean, precise, deep bass even at top volume and a pair of 25mm dome tweeters that produce crystal clear highs. Indoors or out, you can fill a space the size of a tennis court with music.,Futuristic Light Show: With Colors synched to the Beat and with Customizable Strobes and Patterns that dazzle your eyes, party with an unique, immersive Audiovisual experience,Up to 18 hours of play time Party from dusk till dawn with up to 18 hours of play time on a single charge. And if that’s not enough, just swap out the replaceable battery* and keep on dancing. Or if you just need an extra boost, 10 minutes fast charge gets you an extra 2 hours of playtime)"
    },
    {
        "id": 5,
        "name": "Noise Airwave Bluetooth",
        "category": "Audio",
        "Brand":"Noise",
        "price":999 ,
        "tag":"Top Rated",
        "img_url":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSXNZBlPbRJpANnXznb7xVyouTuupmIrZJsJw&s",
        "description": " Noise Newly Launched Airwave Crest Bluetooth in Ear Neckband with Metallic Shine on Earbuds,50H of Playtime, EQ Modes, Dual Device Pairing,13mm PEEK+PU Driver, BT v5.4",
    }
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
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM categories')
    db_categories = cursor.fetchall()
    categories = [
        {"img": row[0], "name": row[1]}
        for row in db_categories
    ]

    featured_products = PRODUCTS[:4]

    # categories from PRODUCTS (clean way)
    

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
    conn=sqlite3.connect('database.db')
    cursor=conn.cursor()
    cursor.execute('''SELECT * FROM categories''')
    db_categories=cursor.fetchall()
    categories = [
        {"img": row[0], "name": row[1]}
        for row in db_categories
    ]

    
    categories_list = ["All"] + sorted({product["name"] for product in categories})
    
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
