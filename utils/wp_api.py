# utils/wp_api.py
import requests
import streamlit as st
from utils.auth import get_basic_auth_headers

# In-memory backup for rollback (for demonstration; production should use persistent storage)
if "backup_log" not in st.session_state:
    st.session_state["backup_log"] = []

def fetch_items(api_base: str, headers: dict, endpoint: str) -> list:
    """Fetch up to 100 items from the given endpoint."""
    try:
        resp = requests.get(f"{api_base}/{endpoint}?per_page=100", headers=headers)
        if resp.status_code == 200:
            return resp.json()
        else:
            return None
    except Exception as e:
        return None

def backup_item(api_base: str, headers: dict, endpoint: str, item_id: str) -> dict:
    """Fetch and return the current state of an item for rollback."""
    try:
        resp = requests.get(f"{api_base}/{endpoint}/{item_id}", headers=headers)
        if resp.status_code == 200:
            backup = resp.json()
            st.session_state["backup_log"].append({"endpoint": endpoint, "id": item_id, "data": backup})
            return backup
        else:
            return {}
    except Exception as e:
        return {}

def update_item(api_base: str, headers: dict, endpoint: str, action: dict) -> (bool, str):
    """Update an existing item. Backs up the original content first."""
    try:
        backup_item(api_base, headers, endpoint, action["id"])
        url = f"{api_base}/{endpoint}/{action['id']}"
        resp = requests.post(url, headers=headers, json=action["changes"])
        if resp.status_code in (200, 201):
            return True, f"ID {action.get('id')} updated."
        else:
            return False, f"HTTP {resp.status_code}: {resp.text}"
    except Exception as e:
        return False, str(e)

def create_item(api_base: str, headers: dict, endpoint: str, action: dict) -> (bool, str):
    """Create a new item."""
    try:
        url = f"{api_base}/{endpoint}"
        resp = requests.post(url, headers=headers, json=action["changes"])
        if resp.status_code in (200, 201):
            return True, f"New item created with ID {resp.json().get('id')}"
        else:
            return False, f"HTTP {resp.status_code}: {resp.text}"
    except Exception as e:
        return False, str(e)

def delete_item(api_base: str, headers: dict, endpoint: str, action: dict) -> (bool, str):
    """Delete an item (backing it up first)."""
    try:
        backup_item(api_base, headers, endpoint, action["id"])
        url = f"{api_base}/{endpoint}/{action['id']}"
        resp = requests.delete(url, headers=headers)
        if resp.status_code in (200, 201):
            return True, f"ID {action.get('id')} deleted."
        else:
            return False, f"HTTP {resp.status_code}: {resp.text}"
    except Exception as e:
        return False, str(e)

def rollback_last_operation() -> (bool, str):
    """
    Roll back the last operation using the backup log.
    For each item in the last backup, re-update the item with its original data.
    """
    if not st.session_state["backup_log"]:
        return False, "No backup available."
    last_backup = st.session_state["backup_log"].pop()
    endpoint = last_backup["endpoint"]
    item_id = last_backup["id"]
    original_data = last_backup["data"]
    wp_site = st.session_state["active_site"]
    api_base = wp_site["site_url"] + "/wp-json/wp/v2"
    headers = get_basic_auth_headers(wp_site["username"], wp_site["app_password"])
    try:
        # Rollback using original title and content.
        changes = {"title": original_data.get("title"), "content": original_data.get("content")}
        url = f"{api_base}/{endpoint}/{item_id}"
        resp = requests.post(url, headers=headers, json=changes)
        if resp.status_code in (200, 201):
            return True, f"ID {item_id} rolled back."
        else:
            return False, f"HTTP {resp.status_code}: {resp.text}"
    except Exception as e:
        return False, str(e)
