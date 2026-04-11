from functools import wraps
import sqlite3
from flask import Flask, flash, redirect, render_template, request, session, url_for
import random
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
        "vd":"https://www.youtube.com/watch?v=q4ZGqdLhuVk",
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
        "vd":"https://www.youtube.com/watch?v=DgsA54_nl94",
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
        "vd":"https://www.youtube.com/watch?v=6wCMVyqBPA8",
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
        "vd":"https://www.youtube.com/watch?v=bny5v3Gt4Xc",
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
        "vd":"https://www.youtube.com/watch?v=m0Gtv71gmKw",
        "img_url":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSXNZBlPbRJpANnXznb7xVyouTuupmIrZJsJw&s",
        "description": " Noise Newly Launched Airwave Crest Bluetooth in Ear Neckband with Metallic Shine on Earbuds,50H of Playtime, EQ Modes, Dual Device Pairing,13mm PEEK+PU Driver, BT v5.4",
    },
    {
        "id": 6,
        "name": "NAME=EVM 16GB DDR4 Laptop",
        "category": "Hardwares",
        "Brand":"EVM",
        "price":9999 ,
        "tag":"Top Rated",
        "vd":"https://www.amazon.in/live/video/13115b5d659c4ff0af853202c41a3413",
        "img_url":"https://m.media-amazon.com/images/I/71pynVlh-oL._AC_UF350,350_QL80_.jpg",
        "description": "Computer Memory Size 16 GB,RAM Memory Technology SODIMM- Laptop RAM,Memory Speed 3200 MHz,Compatible Devices=Laptop",
        "ABOUT":"Fast 16GB DDR4 3200MHz Laptop Memory – Instant Performance Boost: Delivers reliable 3200MHz speed with optimized CL latency for noticeably faster multitasking, smoother gaming, quicker application launches, and snappier overall laptop performance,Universal Laptop Compatibility – 204/260-Pin SO-DIMM: Engineered to work with Intel and AMD laptops including HP, Dell, Lenovo, Asus, Acer, Apple iMac, and more – a straightforward, plug-and-play upgrade requiring no technical expertise,Low Voltage 1.2V Design – Battery-Friendly Operation: Operates at energy-efficient 1.2V, producing less heat and conserving battery life compared to higher-voltage memory, making it ideal for laptop users who need performance on the go",
    },
    {
        "id": 7,
        "name": "Crucial P310 1TB ",
        "category": "Hardwares",
        "Brand":"Crucial",
        "tag":"Hot Deal",
        "price":15999 ,
        "vd":"https://www.youtube.com/watch?v=C60IWHHo8mM",
        "img_url":"https://m.media-amazon.com/images/I/51iNNIdPqkL.jpg",
        "description": "Digital Storage Capacity 1 TB,Hard Disk Interfac PCIE x 4,Connectivity Technology PCIe,Special Feature PCIe Gen4 NVMe Technology, Optimized Power Efficiency,Hard Disk Description Solid State Drive,Compatible Devices Desktop,Installation Type Internal Hard Drive,Hard Disk Size 1 TB ,Specific Uses For Product=Gaming",

    },
    {
        "id": 8,
        "name": "Intel Core i5",
        "category": "Hardwares",
        "Brand":"Intel",
        "price":15499 ,
        "tag":"New Launch",
        "vd":"https://www.youtube.com/watch?v=YyLvipvRFb8",
        "img_url":"https://m.media-amazon.com/images/I/61lNEpDfdcL._AC_UF1000,1000_QL80_.jpg",
        "description":"CPU ManufacturerIntel,CPU Model Core i5-12400F,CPU Speed 4.4 GHz,CPU Socket LGA 1700)"
 
    },

   {
        "id": 9,
        "name": "LANYAO WiFi 6E AX210 NGW Wireless Card",
        "category": "Hardwares",
        "Brand":"LANYAO",
        "price":8130 ,
        "tag":"Hot Deal",
        "vd":"https://www.youtube.com/watch?v=dtNDz-XO8CU",
        "img_url":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS4NnLwtzmOiHHDQRWug28_fPYvYUkmWpIkjQ&s",
        "description": "Hardware Interface Memory Stick Micro (M2),Compatible Devices Laptop,Data Link Protocol IEEE 802.11ac,Data Transfer Rate 5374 Megabits Per SecondItem Weight0.04 Kilograms,Manufacturer==LANYAO)"
},
{ 
      "id": 10,
        "name": "Digital Camera",
        "category": "cameras",
        "Brand":"LEQTRONIQ",
        "price":15999 ,
        "tag":"New Launch",
        "vd":"https://www.youtube.com/watch?v=KtzRJLuzs9g",
        "img_url":"https://m.media-amazon.com/images/I/71UD0DCIVSL._AC_UF1000,1000_QL80_.jpg",
        "description": "Photo Sensor Technology CMOS,Video Capture Resolution 4K, 2.7K, 1080p, 720p,Maximum Focal Length 64 Millimeters ,Maximum Aperture64 Millimeters Flash Memory Type SD Video Capture Format MP4 Supported Audio Format AAC, MP3 Screen Size 4 Inches,Connectivity Technology HDMI, USB, Wi-Fi)"
 
    },

{
        "id": 11,
        "name": "Sony Alpha ILCE-6700M",
        "category": "cameras",
        "Brand":"Sony",
        "price":153990 ,
        "tag":"Hot Deal",
        "vd":"https://www.youtube.com/watch?v=lIQvolP97FM",
        "img_url":"https://m.media-amazon.com/images/I/71NZHYzkyzL._AC_UF1000,1000_QL80_.jpg",
        "description": "Compatible Mountings Sony E Aspect Ratio 1:1, 3:2, 4:3 Photo Sensor Technology CMOS ,Supported File Format=HEIF, JPEG, Raw Image Stabilisation Sensor-shift,Maximum Focal Length 135 Millimeters,Optical Zoom=1 xExpanded ISO Minimum=50,Metering Description=Center Weighted"
    },

    {
        "id": 12,
        "name": "DJI Osmo Pocket 3",
        "category": "cameras",
        "price":40990 ,
        "tag":"Leatest",
        "vd":"https://www.youtube.com/watch?v=MSs7EITvCBs",
        "img_url":"https://www.xboom.in/wp-content/uploads/2025/08/DJI-Pocket-3-1.jpg",
        "description": "Photo Sensor Technology CMOS,Video Capture Resolution 4K,Maximum Focal Length=20 Millimeters Maximum Aperture 2f Flash Memory Type=SmartMedia Video Capture FormatMP4 Supported Audio Format Advanced Audio Codec Screen Size 2 Inches Connectivity Technology=Bluetooth, Wi-Fi"
    },
    {
        "id": 13,
        "name": "GoPro HERO12 ",
        "category": "cameras",
        "Brand":"GoPro",
        "price":29990 ,
        "tag":"New Launch",
        "vd":"https://www.youtube.com/watch?v=UZ5G0tVwBkI",
        "img_url":"https://m.media-amazon.com/images/I/61dUvabnSmL._AC_UF1000,1000_QL80_.jpg",
        "description": "Photo Sensor Technology CMOS Video Capture Resolution 5.3K60/50, 4K120/100, 2.7K240/200, 1080p240/200 resolution/fps3 Maximum Focal Length=30 Millimeters Maximum Aperture 2.8 f Flash Memory Type Micro SD, SD Video Capture Format MP4 Supported Audio Format AAC, MP3, PCM, FLAC, Dolby Digital/AC-3 Screen Size 2.27 Inches Connectivity Technology USB"    
        },
        {
            "id": 14,
        "name": "Irusu Play VR Ultra 3D VR Headset for Mobile",
        "category": "Gaming",
        "price":3099 ,
        "Brand":"IRUSU",
        "tag":"Top Deal",
        "vd":"https://www.youtube.com/watch?v=O0YRW5wkFcs",
        "img_url":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQaOMQdgnmf8dhe4KGuMH9YBwQzau75XJSfXA&s",
        "description": "Specific Uses For Product=For Experiencing the Virtual reality with users mobile Included Components=VR Headset,remote controller Compatible Devices=Smartphone Age Range (Description) Adult Product Dimensions=21D x 23W x 10H Centimeters,Operating System=Android, iOS)"
        
    },
    {
        "id": 15,
        "name": "SpinBot Arcade Wireless Mobile Gamepad",
        "category": "Gaming",
        "Brand":"SpinBot",
        "price": 2949,
        "tag":"POWER DEAL",
        "vd":"https://www.youtube.com/watch?v=zU_LaKh3hVU",
       "img_url":"https://spinbot.co.in/cdn/shop/files/Thumbnail-6_b748607c-0608-4a7e-ac32-087b5e1e8244.jpg?v=1772539731&width=1946",
        "description": "Model Name Arcade Gamepad Compatible Devices Android, IOS, Windows Controller Type=Gamepad Connectivity Technology=Bluetooth)"
  
    },
    {
        "id": 16,
        "name": "ARcNet Dualshock Wireless Controller",
        "category": "Gaming",
        "Brand":"ARcNet",
        "price": 2198,
        "tag":"25% off",
        "vd":"https://www.amazon.in/live/video/175545a9588a4fe9b2e2c38c4aaecd3e",
        "img_url":"https://m.media-amazon.com/images/I/71qFi3hnTHL._AC_UF1000,1000_QL80_.jpg",
        "description": "Model Name=APS-4 Compatible Devices=Playstation 4, Windows, smartphone, tablet Controller Type=Gamepad Connectivity Technology=USB)"

    },
{
        "id": 17,
        "name": "ZEBRONICS PS5SC",
        "category": "Gaming",
        "Brand":"ZEBRONICS",
        "tag":"50% off",
        "price":1999 ,
        "vd":"https://www.youtube.com/watch?v=LqdjMyGFsJ8",
        "img_url":"https://zebronics.com/cdn/shop/files/Zeb-PS5SC-pic4.jpg?v=1749276333&width=2000",
        "description": "Recommended Uses For Product=dock PlayStation and its accessories Colour=white Form Factor=Table Stand Compatible Devices=Gaming Consoles)"
 
    },
    {
        "id": 18,
        "name": "HP Omnibook 5 OLED",
        "category": "laptop",
        "price":69796 ,
        "Brand":"HP",
        "tag":"Hot Deal",
        "vd":"https://www.youtube.com/watch?v=TQOIBbnGGXU",
        "img_url":"https://m.media-amazon.com/images/I/71yaFtjgRzL._AC_UF1000,1000_QL80_.jpg",
        "description": "HP Laptop Screen 40.6 cm Colour Glacier Silver1 TB Snapdragon X 16 GB Windows 11 Home AI Assistant, Fast Charge Integrated Graphics Card"  
 
    },
{
        "id": 19,
        "name": "ASUS Vivobook 14",
        "category": "laptop",
        "price":72990 ,
        "tag":"slim ",
        "Brand":"ASUS",
        "vd":"https://www.youtube.com/watch?v=jU9ad2C0EDI",
        "img_url":"https://m.media-amazon.com/images/I/418dOHs7XKL._AC_UF1000,1000_QL80_.jpg",
        "description": "ASUS Vivobook  14 Intel Core Ultra 5 Processor 225H 1.7 GHz 14 Inche 1 TB SSD 16 GB RAM Windows 11 Home Integrated Graphics Card "
},

{
        "id": 20,
        "name": "Samsung Galaxy Book6 Pro",
        "category": "laptop",
        "price":214990 ,
        "tag":"Super Deal",
        "Brand":"Samsung",
        "vd":"https://www.youtube.com/watch?v=U8og9S3fKXs",
        "img_url":"data:image/webp;base64,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",
        "description": "Galaxy Book6 Pro 14 Inches Gray 1024 GB Intel Core Ultra X7 32 GB Windows 11 Home Integrated Graphics Card HD Audio, Lightweight"
  
    },
{
        "id": 21,
        "name": "acer Nitro Lite 16",
        "category": "laptop",
        "price":84750 ,
        "tag":"New Offers",
        "Brand":"acer",
        "vd":"https://www.youtube.com/watch?v=9ZVbdBObJLM",
        "img_url":"https://m.media-amazon.com/images/I/81ShI4duOGL.jpg",
        "description": "NITRO LITE 16 16 Inches White 512 GB Intel Core i7-13620H 16 GB Windows 11 Home Backlit Keyboard NVIDIA GeForce RTX 3050 with 6GB)"
},
{
    "id": 22,
    "name": "Lenovo IdealPad Slim 5 ",
    "category": "laptop",
    "price": 64990 ,
    "tag":"New Edition",
    "Brand":"Lenovo",
     "vd":"https://www.youtube.com/watch?v=9ZVbdBObJLM",
     "img_url":"data:image/webp;base64,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",
     "description": " Lenovo IdeaPad Slim 5 Intel Core Ultra 5 125H 16 (40.6cm) WUXGA-IPS 300Nits Thin & Light Laptop (16GB RAM/1TB SSD/AI PC/Windows 11/Office Home 2024/FHD+IR Camera/1Yr ADP Free/Grey/1.8Kg), 83DC0096IN"
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

    featured_products = random.sample(PRODUCTS, 4)

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
    selected_brand=request.args.get("brand")
    price_range=request.args.get("price_range")
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
    if selected_brand:
        filtered_products = [
            p for p in filtered_products
            if p.get("Brand") == selected_brand
        ]
    if price_range:
        min_price, max_price = map(int, price_range.split("-"))
        filtered_products = [
            p for p in filtered_products
            if min_price <= p["price"] <= max_price
        ]
    if selected_category =="All":
        brands = sorted({p.get("Brand") for p in PRODUCTS if p.get("Brand")})
    else:
        brands=sorted({ p.get("Brand") for p in PRODUCTS if p.get("Brand") and p.get("category") == selected_category})

    
    #filter_brand=[  product["Brand"]for product in PRODUCTS ]
    return render_template(
        "categories.html",
        brands=brands,
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
