import streamlit as st
import pandas as pd
import os
import time

FILE_PATH = "chocalates.xlsx"

st.set_page_config(page_title="CocoCart Fancy Shop", layout="wide")

# Load inventory
@st.cache_data(ttl=60)
def load_data():
    if os.path.exists(FILE_PATH):
        return pd.read_excel(FILE_PATH)
    else:
        return pd.DataFrame(columns=["Name", "Price", "Quantity", "Image URL"])

df = load_data()

# Initialize cart and purchase flags
if "cart" not in st.session_state:
    st.session_state.cart = []
if "purchase_complete" not in st.session_state:
    st.session_state.purchase_complete = False

# Sidebar: Navigation + Cart
st.sidebar.title("🧭 Menu")
selected_page = st.sidebar.radio("Go to", ["Shop", "Admin"])

st.sidebar.title("🛒 Cart")
if not st.session_state.cart:
    st.sidebar.info("Cart is empty")
else:
    total = 0
    cart_summary = {}
    for idx in st.session_state.cart:
        row = df.iloc[idx]
        cart_summary[idx] = cart_summary.get(idx, 0) + 1
        total += row["Price"]

    for idx, count in cart_summary.items():
        row = df.iloc[idx]
        st.sidebar.write(f"{row['Name']} x{count} - ₹{row['Price']}")

    if st.sidebar.button("Buy Now 💳"):
        for idx, count in cart_summary.items():
            df.at[idx, "Quantity"] = max(df.at[idx, "Quantity"] - count, 0)
        df.to_excel(FILE_PATH, index=False)
        st.session_state.cart.clear()
        st.session_state.purchase_complete = True
        st.rerun()

# Show Thank You after purchase
if st.session_state.purchase_complete:
    st.sidebar.success("Thanks for buying! 🎉")
    st.balloons()
    time.sleep(2)
    st.session_state.purchase_complete = False
    st.rerun()

# Top bar + nav + search
st.markdown("""
    <style>
        .top-bar {
            background-color: black;
            padding: 1rem 2rem;
            color: white;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .nav {
            margin-top: 10px;
            display: flex;
            justify-content: center;
            gap: 30px;
            font-size: 1.1rem;
            font-weight: bold;
        }
        .nav a {
            color: black;
            text-decoration: none;
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
        <a href='#'>BIRTHDAY GIFTS</a>
        <a href='#'>CHOCOLATE</a>
        <a href='#'>HOT CHOCOLATE</a>
        <a href='#'>VELVETISER</a>
        <a href='#'>ALCOHOL</a>
        <a href='#'>SUBSCRIPTIONS</a>
    </div>
""", unsafe_allow_html=True)

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
            background-image: url('banner_1.png');
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
        <a href='#'>ALCOHOL</a>
        <a href='#'>SUBSCRIPTIONS</a>
    </div>

    <div class='hero'>
        <h1>A STORY IN EVERY GIFT</h1>
        <p>Crafted with care, curated with love.<br>Indulge in a luxury chocolate experience.</p>
        <button class="shop-now">SHOP NOW</button>
        <button class="gifting">GIFTING OPTIONS</button>
    </div>

    <div class='section'>
        <h2>🍫 Our Chocolate Collection</h2>
        <p>Browse our handpicked selection of rich, decadent chocolates perfect for every occasion.</p>
    </div>
""", unsafe_allow_html=True)

# Shop Page
if selected_page == "Shop":
    st.markdown("## 🍫 Shop Chocolates")

    for idx, row in df.iterrows():
        with st.container():
            cols = st.columns([2, 3, 1])
            with cols[0]:
                if "Image URL" in df.columns and pd.notna(row["Image URL"]):
                    st.image(row["Image URL"], width=200)
                else:
                    st.image("https://via.placeholder.com/200x150.png?text=No+Image", width=200)
            with cols[1]:
                st.markdown(f"### {row['Name']}")
                st.markdown(f"💰 ₹{row['Price']}")
            with cols[2]:
                if row["Quantity"] > 0:
                    if st.button("Add to Cart", key=f"add_{idx}"):
                        st.session_state.cart.append(idx)
                        st.rerun()
                else:
                    st.error("Out of Stock")


# Admin Page
elif selected_page == "Admin":
    st.title("🧑‍💼 Inventory Management")
    st.dataframe(df[["Name", "Price", "Quantity"]], use_container_width=True)

    with st.expander("🔄 Refresh Inventory"):
        if st.button("Reload Data"):
            st.cache_data.clear()
            st.rerun()

