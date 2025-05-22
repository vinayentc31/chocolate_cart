import streamlit as st
import pandas as pd

# Top nav + hero + style
st.markdown("""
    <style>
        body { background-color: #fffaf8; }
        .top-bar {
            background-color: black;
            padding: 1rem 2rem;
            color: white;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-family: 'Helvetica Neue', sans-serif;
        }
        .nav {
            margin: 20px auto;
            text-align: center;
        }
        .nav a {
            margin: 0 20px;
            color: #333;
            font-weight: bold;
            text-decoration: none;
        }
        .hero {
            background-image: url('https://www.hotelchocolat.com/on/demandware.static/-/Sites-HotelChocolat-Library/default/dw388df5bd/HC/2024/Core/500px-Images/birthdays24-macarons-hp-sq-500px.webp');
            background-size: cover;
            background-position: center;
            color: white;
            border-radius: 12px;
            padding: 5rem 2rem;
            text-align: left;
            margin-top: 20px;
        }
        .hero h1 { font-size: 3.5rem; margin-bottom: 10px; }
        .hero p { font-size: 1.2rem; }
        .hero button {
            padding: 0.75rem 1.5rem;
            margin-right: 10px;
            font-size: 1rem;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        .shop-now { background-color: white; color: black; }
        .gifting { background: transparent; border: 1px solid white; color: white; }

        .section {
            padding: 3rem 1rem;
            text-align: center;
        }
        .section img {
            width: 100%;
            border-radius: 10px;
            margin-top: 1rem;
        }

        .product-scroll {
            display: flex;
            overflow-x: auto;
            gap: 20px;
            padding: 20px 0;
        }
        .product-card {
            min-width: 250px;
            background-color: #fff7f7;
            border-radius: 12px;
            padding: 1rem;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
            text-align: center;
        }
        .product-card img {
            width: 100%;
            border-radius: 10px;
            margin-bottom: 10px;
        }
        .product-card h3 {
            font-size: 1.2rem;
            margin: 0.5rem 0;
            color: #4e342e;
        }

        .footer {
            background-color: #1c1c1c;
            color: white;
            padding: 3rem 1rem;
            font-size: 0.9rem;
        }
        .footer-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 30px;
        }
        .footer-section h4 {
            font-size: 1.1rem;
            margin-bottom: 1rem;
            border-bottom: 1px solid #444;
            padding-bottom: 0.5rem;
        }
        .footer-section ul {
            list-style: none;
            padding: 0;
        }
        .footer-section ul li {
            margin: 6px 0;
        }
    </style>

    <div class='top-bar'>
        <div>📍 Locations | ❓ Help</div>
        <div><h2 style='margin:0;'>Hotel CocoCart</h2></div>
        <div>👤 Login | 🛍️ Cart</div>
    </div>

    <div class='nav'>
        <a href='#'>SUMMER</a>
        <a href='#'>GIFT IDEAS</a>
        <a href='#'>CHOCOLATE</a>
        <a href='#'>VELVETISER</a>
        <a href='#'>SUBSCRIPTIONS</a>
    </div>

    <div class='hero'>
        <h1>A STORY IN EVERY GIFT</h1>
        <p>Crafted with care, curated with love.<br>Indulge in a luxury chocolate experience.</p>
        <button class="shop-now">SHOP NOW</button>
        <button class="gifting">GIFTING OPTIONS</button>
    </div>

""", unsafe_allow_html=True)
# Load products
# @st.cache_data
def load_products():
    return pd.read_excel("products.xlsx")  # Always loads fresh copy

def save_products(df):
    df.to_excel("products.xlsx", index=False)

# --- Session State ---
if "cart" not in st.session_state:
    st.session_state.cart = {}

# --- Add to Cart function ---
def add_to_cart(product_id):
    cart = st.session_state.cart
    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1


# --- Sidebar Menu ---
page = st.sidebar.selectbox("Menu", ["Shop", "Admin"])





if page == "Shop":
    df = load_products()
    cols = st.columns(3)
    for index, row in df.iterrows():
        with cols[index % 3]:
            st.image(row["image_url"], use_container_width=True)
            st.subheader(row["name"])
            st.caption(row["description"])
            st.write(f"💵 ${row['price']:.2f}")
            st.write(f"⭐⭐⭐⭐☆")
            if row["quantity"] <= 0:
                st.button("Out of Stock", key=f"out_{row['id']}", disabled=True)
            else:
                if st.button("Add to Cart", key=f"add_{row['id']}"):
                    add_to_cart(row["id"])
                    st.success(f"Added {row['name']} to cart!")

    st.markdown("---")

    # --- Cart in Sidebar ---
    st.sidebar.header("🛒 Your Cart")
    cart = st.session_state.cart
    df = load_products()

    if not cart:
        st.sidebar.write("Cart is empty.")
    else:
        total = 0
        cart_df = df[df["id"].isin(cart.keys())].copy()
        for i, row in cart_df.iterrows():
            qty = cart[row["id"]]
            subtotal = qty * row["price"]
            total += subtotal
            st.sidebar.write(f"{row['name']} x {qty} = ${subtotal:.2f}")
        st.sidebar.write(f"**Total: ${total:.2f}**")

        if st.sidebar.button("Buy Now"):
            out_of_stock = False
            for i, row in cart_df.iterrows():
                qty_in_cart = cart[row["id"]]
                if qty_in_cart > row["quantity"]:
                    st.sidebar.error(f"Not enough stock for {row['name']}")
                    out_of_stock = True

            if not out_of_stock:
                for i, row in cart_df.iterrows():
                    product_id = row["id"]
                    qty_in_cart = cart[product_id]
                    df.loc[df["id"] == product_id, "quantity"] -= qty_in_cart

                save_products(df)
                st.sidebar.success("Purchase complete!")

                # Clear the cart after purchase:
                st.session_state["cart"] = {}

                # Force UI to refresh and show empty cart immediately:
                st.rerun()


elif page == "Admin":
    st.title("⚙️ Admin Panel - Manage Products")

    df = load_products()  # ✅ Load fresh data here

    for i, row in df.iterrows():
        st.write(f"**ID:** {row['id']} - **{row['name']}**")
        new_name = st.text_input(f"Name (ID {row['id']})", row["name"], key=f"name_{row['id']}")
        new_desc = st.text_area(f"Description (ID {row['id']})", row["description"], key=f"desc_{row['id']}")
        new_price = st.number_input(f"Price (ID {row['id']})", min_value=0.0, value=row["price"], step=0.01, format="%.2f", key=f"price_{row['id']}")
        new_qty = st.number_input(f"Quantity (ID {row['id']})", min_value=0, value=int(row["quantity"]), step=1, key=f"qty_{row['id']}")
        new_img = st.text_input(f"Image URL (ID {row['id']})", row["image_url"], key=f"img_{row['id']}")

        if (new_name != row["name"] or new_desc != row["description"] or
            new_price != row["price"] or new_qty != row["quantity"] or
            new_img != row["image_url"]):
            df.loc[df["id"] == row["id"], ["name", "description", "price", "quantity", "image_url"]] = \
                [new_name, new_desc, new_price, new_qty, new_img]

    if st.button("Save Changes"):
        save_products(df)
        st.success("Changes saved!")
        st.rerun()  # ⭯ Refresh to load updated data

    # Add new product
    st.subheader("➕ Add New Product")
    new_id = int(df["id"].max()) + 1 if not df.empty else 1
    new_name = st.text_input("Name", key="new_name")
    new_desc = st.text_area("Description", key="new_desc")
    new_price = st.number_input("Price", min_value=0.0, step=0.01, format="%.2f", key="new_price")
    new_qty = st.number_input("Quantity", min_value=0, step=1, key="new_qty")
    new_img = st.text_input("Image URL", key="new_img")

    if st.button("Add Product"):
        if new_name and new_desc and new_img:
            new_row = {
                "id": new_id,
                "name": new_name,
                "description": new_desc,
                "price": new_price,
                "quantity": new_qty,
                "image_url": new_img
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            save_products(df)
            st.success(f"✅ Added product '{new_name}'")
            st.rerun()
        else:
            st.error("❗ Please fill in all product fields.")
