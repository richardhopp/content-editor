# utils/auth.py
import json, os
import streamlit as st
from cryptography.fernet import Fernet

def get_fernet():
    key = st.secrets.get("credentials", {}).get("ENCRYPT_KEY")
    if key:
        return Fernet(key.encode())
    else:
        st.error("ENCRYPT_KEY not set in secrets.")
        st.stop()

def encrypt_data(data: dict) -> bytes:
    f = get_fernet()
    return f.encrypt(json.dumps(data).encode())

def decrypt_data(data_bytes: bytes) -> dict:
    f = get_fernet()
    return json.loads(f.decrypt(data_bytes).decode())

def load_sites():
    SITES_FILE = "sites.enc"
    if os.path.exists(SITES_FILE):
        with open(SITES_FILE, "rb") as f:
            enc = f.read()
        try:
            return decrypt_data(enc)
        except Exception as e:
            st.error("Error decrypting saved sites.")
            return []
    else:
        return []

def save_sites(sites: list):
    SITES_FILE = "sites.enc"
    with open(SITES_FILE, "wb") as f:
        f.write(encrypt_data(sites))

def get_basic_auth_headers(username: str, app_password: str) -> dict:
    import base64
    token = base64.b64encode(f"{username}:{app_password}".encode()).decode()
    return {"Authorization": f"Basic {token}"}

def test_wp_connection(api_base: str, headers: dict) -> bool:
    import requests
    try:
        resp = requests.get(api_base + "/posts?per_page=1", headers=headers)
        return resp.status_code < 400
    except Exception as e:
        return False
