# pages/2_OwnerPanel.py
import streamlit as st
import json
import pandas as pd
from utils.auth import load_sites
from utils.logger import get_recent_errors

if st.session_state.get("role") != "Owner":
    st.error("Access denied. Owner only.")
    st.stop()

st.header("Owner Settings")
st.markdown("This panel is for the Owner only. Adjust advanced functionality, view logs, and trigger rollback.")

st.subheader("Advanced AI Override")
owner_override = st.text_area("Custom AI Override Prompt", placeholder="Enter system-level instructions for AI behavior.")
if st.button("Save Override"):
    if owner_override.strip():
        st.session_state["ai_override"] = owner_override.strip()
        st.success("Override saved. Future AI commands will include these instructions.")
    else:
        st.error("Override cannot be empty.")

st.subheader("Revert to Default Functionality")
if st.button("Revert to Default Code"):
    if "ai_override" in st.session_state:
        del st.session_state["ai_override"]
    st.success("Reverted to default functionality.")

st.subheader("Saved Site Credentials")
sites = load_sites()
if sites:
    st.json(sites)
else:
    st.write("No sites saved.")

st.subheader("Recent Error Log")
errors = get_recent_errors()
if errors:
    st.table(pd.DataFrame(errors))
else:
    st.info("No errors logged.")

st.subheader("Rollback Changes")
if st.button("Rollback Last Operation"):
    from utils.wp_api import rollback_last_operation
    success, msg = rollback_last_operation()
    if success:
        st.success("Rollback successful.")
    else:
        st.error(f"Rollback failed: {msg}")

st.markdown("**Note:** Only the Owner can modify system settings and trigger rollbacks.")
