import streamlit as st
import pandas as pd
import os

FILE_PATH = "chocalates.xlsx"

# Set page config at the very top
st.set_page_config(page_title="CocoCart Fancy Shop", layout="wide")
# --- Fancy Banner / Hero Section ---
st.markdown("""
    <div style='background-color: #ffebee; padding: 40px 10px; border-radius: 12px; text-align: center; box-shadow: 0 4px 10px rgba(0,0,0,0.1); margin-bottom: 30px;'>
        <h1 style='font-size: 3em; color: #4a148c; margin: 0;'>🍫 Welcome to CocoCart 🍫</h1>
        <p style='font-size: 1.3em; color: #6a1b9a;'>Your one-stop shop for delicious chocolate delights</p>
    </div>
""", unsafe_allow_html=True)

# Load inventory
@st.cache_data(ttl=60)
def load_data():
    if os.path.exists(FILE_PATH):
        return pd.read_excel(FILE_PATH)
    else:
        return pd.DataFrame(columns=["Name", "Price", "Quantity", "Image URL"])

df = load_data()

# Initialize cart in session
if "cart" not in st.session_state:
    st.session_state.cart = []

# Sidebar: Navigation + Cart Panel
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

    # Handle purchase
    if st.sidebar.button("Buy Now 💳"):
        for idx, count in cart_summary.items():
            df.at[idx, "Quantity"] = max(df.at[idx, "Quantity"] - count, 0)
        df.to_excel(FILE_PATH, index=False)
        st.session_state.cart.clear()
        
        # Set flag that purchase was completed
        st.session_state.purchase_complete = True

    # Show purchase success
    if st.session_state.get("purchase_complete", False):
        st.sidebar.success("Thanks for buying! 🎉")
        st.balloons()

        # Add a small delay using a placeholder + rerun after short time
        import time
        time.sleep(1)  # Wait 1 seconds before rerunning (just enough for message & balloons)
        
        st.session_state.purchase_complete = False
        st.rerun()



# Shop Page
if selected_page == "Shop":
    st.title("🍫 Welcome to CocoCart")

    for idx, row in df.iterrows():
        with st.container():
            cols = st.columns([2, 2, 1])
            with cols[0]:
                if "Image URL" in df.columns and pd.notna(row["Image URL"]):
                    st.image(row["Image URL"], width=200)
                else:
                    st.image("https://via.placeholder.com/200x150.png?text=No+Image", width=200)
            with cols[1]:
                st.subheader(row["Name"])
                st.write(f"💰 Price: ₹{row['Price']}")
            with cols[2]:
                if row["Quantity"] > 0:
                    if st.button("Add to Cart", key=f"add_{idx}"):
                        st.session_state.cart.append(idx)
                        st.rerun()  # Reruns the app to reflect cart update
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
