import streamlit as st
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from connectors.cars24 import Cars24Scraper
from connectors.olx import OlxScraper
from connectors.cardekho import CardekhoScraper
from normalize import normalize_listing
from sheets import get_sheet
from datetime import datetime

def login():
    st.set_page_config(page_title="Admin Login", layout="centered")
    st.title("🔐 Admin Login")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            if username == "Usedcaradmin" and password == "admin@123":
                st.session_state["logged_in"] = True
            else:
                st.session_state["logged_in"] = False
                st.error("Invalid credentials")


# --- Show login page if not logged in ---
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    login()
    st.stop()

# 🎯 Setup
st.set_page_config(page_title="Used Car Aggregator", layout="wide")
st.title("Used Car Price Aggregator")
current_year = datetime.now().year

# 🚗 Sidebar Filters
with st.sidebar:
    st.header("Search Filters")

    brand = st.selectbox("Car Brand", ["Honda", "Hyundai", "Maruti-suzuki", "Tata", "Mahindra", "Toyota"])
    model = st.selectbox("Car Model", {
        "Honda": ["City", "Amaze", "Jazz", "Brio"],
        "Hyundai": ["i20", "Creta", "Verna", "Santro"],
        "Maruti-suzuki": ["Swift", "Baleno", "Dzire", "Alto"],
        "Tata": ["Nexon", "Harrier", "Altroz", "Tiago"],
        "Mahindra": ["XUV500", "Scorpio", "Thar", "Bolero"],
        "Toyota": ["Innova", "Fortuner", "Corolla", "Glanza"]
    }.get(brand, []))

    transmission = st.selectbox("Transmission", ["", "manual", "automatic"])
    fuel = st.selectbox("Fuel Type", ["", "petrol", "diesel", "cng", "electric"])
    city = st.text_input("City", "Bangalore")
    min_year = st.selectbox("Min Year", range(current_year - 20, current_year))
    max_year = st.selectbox("Max Year", range(current_year, current_year - 20, -1))
    budget_min = st.selectbox("Min Budget (₹)", range(100000, 3000000, 100000))
    budget_max = st.selectbox("Max Budget (₹)", range(5000000, 200000, -100000))
    run_search = st.button("🔍 Search Cars")

# 🧮 Filters Dictionary
filters = {
    "brand": brand, "model": model, "transmission": transmission, "fuel": fuel,
    "city": city, "year_min": min_year, "year_max": max_year,
    "budget_min": budget_min, "budget_max": budget_max
}

# 🔍 Search Logic
if run_search:
    st.info("Fetching live listings... Please wait ⏳")
    scrapers = [("Cars24", Cars24Scraper()), ("OLX", OlxScraper()), ("Cardekho", CardekhoScraper())]

    def fetch(name_scraper):
        name, scraper = name_scraper
        try:
            results = scraper.fetch_listings(filters)
            msg = f"{name} returned {len(results)} listings" if results else f"No filtered cars in {name}"
            return [normalize_listing(r) for r in results], msg
        except Exception as e:
            return [], f"Error in {name}: {e}"

    all_data = []
    for listings, msg in ThreadPoolExecutor().map(fetch, scrapers):
        st.info(msg)
        all_data.extend(listings)

    df = pd.DataFrame(all_data)

    # 📊 Display Results
    if df.empty:
        st.warning("No listings found with the given filters.")
    else:
        df = df[df["price_inr"].between(budget_min, budget_max)]
        st.markdown(df.to_markdown(), unsafe_allow_html=True)

        # 📤 Export to Google Sheets
        try:
            sheet = get_sheet()
            sheet.clear()
            sheet.update([df.columns.tolist()] + df.values.tolist())
            st.info("Results exported to Google Sheets")
            st.success("https://docs.google.com/spreadsheets/d/1ZZf9xo-HTlNehV-hISL2FQHOCS8nOd9yMNY___pG-KE/edit?gid=0#gid=0")
        except Exception as e:
            st.error(f"Google Sheets export failed: {e}")
