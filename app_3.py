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
            background-image: url('https://your-hero-image-url.jpg');
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

# Product Section (Scrollable)
st.markdown("<div class='product-scroll'>", unsafe_allow_html=True)
for idx, row in df.iterrows():
    with st.container():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"""
                <div class='product-card'>
                    <img src="{row['Image URL'] if pd.notna(row['Image URL']) else 'https://via.placeholder.com/250x180.png?text=No+Image'}" />
                    <h3>{row['Name']}</h3>
                    <p>₹{row['Price']}</p>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            if row["Quantity"] > 0:
                if st.button("Add to Cart", key=f"add_{idx}"):
                    st.session_state.cart.append(idx)
                    st.rerun()
            else:
                st.error("Out of Stock")
st.markdown("</div>", unsafe_allow_html=True)

# Extra Image-Based Sections
st.markdown("""
    <div class='section'>
        <h2>☕ Velvetised Drinking Chocolates</h2>
        <p>Barista-grade indulgence, made at home. Serve hot or chilled over ice.</p>
        <img src='https://your-velvetiser-image.jpg' />
    </div>

    <div class='section'>
        <h2>🎁 Gifting Made Easy</h2>
        <p>Choose beautifully wrapped options for every celebration, big or small.</p>
        <img src='https://your-gift-wrap-image.jpg' />
    </div>

    <div class='section'>
        <h2>🚚 Free Delivery on All Orders</h2>
        <p>Enjoy doorstep delivery anywhere in the country — on us.</p>
        <img src='https://your-delivery-image.jpg' />
    </div>

    <div class='footer'>
        <div class='section' style='text-align: center;'>
            <h2>LET US TREAT YOUR INBOX</h2>
            <input type='text' placeholder='Enter Your Email Address here...' style='padding: 0.7rem 1rem; width: 300px; margin-top: 1rem;'>
        </div>
        <div class='footer-grid'>
            <div class='footer-section'>
                <h4>ABOUT US</h4>
                <ul>
                    <li>Our Story</li>
                    <li>Ethics & Sustainability</li>
                    <li>Corporate Responsibility</li>
                    <li>VIP.ME</li>
                </ul>
            </div>
            <div class='footer-section'>
                <h4>HELP CENTRE</h4>
                <ul>
                    <li>FAQs</li>
                    <li>Returns</li>
                    <li>Gift Cards</li>
                    <li>Delivery</li>
                </ul>
            </div>
            <div class='footer-section'>
                <h4>WORK WITH US</h4>
                <ul>
                    <li>Careers</li>
                    <li>Affiliates</li>
                    <li>Press</li>
                </ul>
            </div>
            <div class='footer-section'>
                <h4>FOLLOW US</h4>
                <ul>
                    <li>Facebook</li>
                    <li>Instagram</li>
                    <li>X (Twitter)</li>
                    <li>Pinterest</li>
                </ul>
            </div>
        </div>
        <div class='section' style='text-align:center; margin-top: 2rem;'>
            <img src='https://your-trustpilot-image-url.jpg' alt='Trustpilot Rating' style='width: 200px;'>
        </div>
    </div>
""", unsafe_allow_html=True)

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
        st.sidebar.markdown(f"**{row['Name']}** x{count} – ₹{row['Price']}")

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