import requests
import streamlit as st

API_BASE_URL = st.text_input("API Base URL", value="http://localhost:8000")

st.title("Menu")
category = st.selectbox("Category", ["all", "burger", "side", "drink"])

params = {}
if category != "all":
    params["category"] = category

if st.button("Load Menus"):
    try:
        response = requests.get(f"{API_BASE_URL}/menus", params=params, timeout=5)
        response.raise_for_status()
        menus = response.json()
        st.success(f"Loaded {len(menus)} menu items")
        st.json(menus)
    except requests.RequestException as exc:
        st.error(f"API request failed: {exc}")
