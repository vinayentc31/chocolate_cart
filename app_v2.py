import streamlit as st
import pandas as pd
import os
import time

FILE_PATH = "chocolates.xlsx"

st.set_page_config(page_title="Hotel CocoCart", layout="wide")

@st.cache_data(ttl=60)
def load_data():
    if os.path.exists(FILE_PATH):
        return pd.read_excel(FILE_PATH)
    else:
        return pd.DataFrame(columns=["Name", "Price", "Quantity", "Image URL"])

df = load_data()

if "cart" not in st.session_state:
    st.session_state.cart = []
if "purchase_complete" not in st.session_state:
    st.session_state.purchase_complete = False

# Custom styles for luxury theme
st.markdown("""
    <style>
        body { background-color: #fffaf8; font-family: 'Georgia', serif; }
        .top-bar {
            background-color: black;
            padding: 1rem 2rem;
            color: white;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 1.3rem;
        }
        .nav {
            margin-top: 10px;
            text-align: center;
        }
        .nav a {
            margin: 0 15px;
            color: #4e342e;
            font-weight: bold;
            text-decoration: none;
        }
        .hero {
            background-image: url('https://your-banner-image-url.jpg');
            background-size: cover;
            background-position: center;
            color: white;
            padding: 5rem 2rem;
            text-align: left;
            border-radius: 12px;
            font-size: 2.5rem;
            font-weight: bold;
        }
        .product-scroll {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
            gap: 30px;
            padding: 2rem;
        }
        .product-card {
            background-color: #fffdfc;
            border-radius: 12px;
            padding: 1rem;
            box-shadow: 0 8px 20px rgba(0,0,0,0.08);
            text-align: center;
            border: 1px solid #eee;
        }
        .product-card img {
            width: 100%;
            height: 180px;
            object-fit: cover;
            border-radius: 10px;
            margin-bottom: 10px;
        }
        .product-card h3 {
            font-size: 1.1rem;
            margin: 0.5rem 0 0.2rem;
            color: #3e2723;
        }
        .stars {
            color: gold;
            margin-bottom: 0.3rem;
        }
        .product-card .price {
            font-weight: bold;
            margin: 0.5rem 0;
            color: #6d4c41;
        }
        .product-card button {
            background-color: #4e342e;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 0.5rem 1rem;
            font-size: 1rem;
            cursor: pointer;
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class='top-bar'>
        <div>🍫 Hotel CocoCart</div>
        <div><a href='?page=admin' style='color:white;'>Admin</a> | Cart</div>
    </div>
    <div class='nav'>
        <a href='?page=home'>HOME</a>
        <a href='#'>COLLECTIONS</a>
        <a href='#'>GIFTING</a>
        <a href='#'>ABOUT</a>
        <a href='#'>CONTACT</a>
    </div>
""", unsafe_allow_html=True)

# Page Routing
page = st.query_params.get("page", "home")

if page == "home":
    st.markdown("""
        <div class='hero'>
            A Story in Every Gift
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='product-scroll'>", unsafe_allow_html=True)
    for idx, row in df.iterrows():
        st.markdown(f"""
            <div class='product-card'>
                <img src="{row['Image URL'] if pd.notna(row['Image URL']) else 'https://via.placeholder.com/300x200.png?text=No+Image'}" />
                <h3>{row['Name']}</h3>
                <div class='stars'>⭐⭐⭐⭐☆</div>
                <p class='price'>₹{row['Price']}</p>
        """, unsafe_allow_html=True)
        if row["Quantity"] > 0:
            if st.button("Add to Cart", key=f"add_{idx}"):
                st.session_state.cart.append(idx)
                st.rerun()
        else:
            st.markdown("<p style='color:red;'>Out of Stock</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

elif page == "admin":
    st.title("🛠️ Admin Panel")
    st.dataframe(df, use_container_width=True)
    if st.button("Refresh Inventory"):
        st.cache_data.clear()
        st.rerun()

# Sidebar Cart
st.sidebar.title("🛒 Your Cart")
if not st.session_state.cart:
    st.sidebar.info("Cart is empty.")
else:
    total = 0
    cart_summary = {}
    for idx in st.session_state.cart:
        row = df.iloc[idx]
        cart_summary[idx] = cart_summary.get(idx, 0) + 1
        total += row["Price"]

    for idx, count in cart_summary.items():
        row = df.iloc[idx]
        st.sidebar.markdown(f"**{row['Name']}** x{count} – ₹{row['Price']} each")

    st.sidebar.markdown(f"### Total: ₹{total}")

    if st.sidebar.button("Buy Now 💳"):
        for idx, count in cart_summary.items():
            df.at[idx, "Quantity"] = max(df.at[idx, "Quantity"] - count, 0)
        df.to_excel(FILE_PATH, index=False)
        st.session_state.cart.clear()
        st.session_state.purchase_complete = True
        st.rerun()

if st.session_state.purchase_complete:
    st.success("🎉 Thank you for your purchase! Enjoy your chocolates.")
    st.balloons()
    time.sleep(2)
    st.session_state.purchase_complete = False
    st.rerun()
