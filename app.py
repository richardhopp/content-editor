# app.py
import streamlit as st
from utils.auth import load_sites, save_sites, get_basic_auth_headers, test_wp_connection
import os

st.set_page_config(page_title="AI WP Content Manager", layout="wide")
st.title("AI WordPress Content Manager")

# --- User Role Selection ---
if "role" not in st.session_state:
    st.subheader("Select User Role")
    role_choice = st.radio("Choose your role:", ["Normal User", "Owner"])
    if role_choice == "Owner":
        owner_pw = st.text_input("Enter Owner Password", type="password")
        if st.button("Submit Role"):
            if owner_pw == st.secrets["credentials"]["owner_password"]:
                st.session_state["role"] = "Owner"
                st.success("Owner mode activated.")
            else:
                st.error("Incorrect Owner Password.")
    else:
        st.session_state["role"] = "Normal User"

# --- Site Management in Sidebar ---
st.sidebar.header("WordPress Site Management")
sites = load_sites()  # load list of site dictionaries
site_names = [site["site_url"] for site in sites] if sites else []

active_site = None
if site_names:
    selected_site = st.sidebar.selectbox("Active Site", options=site_names)
    active_site = next((site for site in sites if site["site_url"] == selected_site), None)

with st.sidebar.expander("Add a New Site"):
    new_site_url = st.text_input("Site URL (e.g., https://example.com)", key="new_site_url")
    new_username = st.text_input("Username", key="new_username")
    new_app_pass = st.text_input("Application Password", type="password", key="new_app_pass")
    if st.button("Save New Site"):
        if new_site_url and new_username and new_app_pass:
            api_base = new_site_url.rstrip("/") + "/wp-json/wp/v2"
            headers = get_basic_auth_headers(new_username, new_app_pass)
            if test_wp_connection(api_base, headers):
                new_site = {
                    "site_url": new_site_url.rstrip("/"),
                    "username": new_username,
                    "app_password": new_app_pass
                }
                sites.append(new_site)
                save_sites(sites)
                st.success("Site added successfully!")
            else:
                st.error("Failed to connect. Check your credentials and site URL.")
        else:
            st.error("Please fill in all fields.")

if active_site:
    st.sidebar.info(f"Connected to: {active_site['site_url']}")
    st.session_state["active_site"] = active_site
else:
    st.sidebar.warning("No active site selected. Please add a site.")

st.markdown("Use the sidebar menu to navigate between Content Editor and Owner Settings.")
st.write("Select a page from the sidebar.")
