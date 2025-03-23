# pages/1_ContentEditor.py
import streamlit as st
import requests, time, re, json, pandas as pd
from utils.wp_api import fetch_items, update_item, create_item, delete_item
from utils.ai import process_prompt_via_openai
from utils.file_utils import parse_csv, parse_excel, parse_text
from utils.scraper import scrape_website

st.header("Content Editor")
st.markdown("Enter your natural language command to create, update, or delete content on your active WordPress site.")

if "active_site" not in st.session_state:
    st.error("No active site selected. Please add/select a site from the sidebar.")
    st.stop()

wp_site = st.session_state["active_site"]
api_base = wp_site["site_url"] + "/wp-json/wp/v2"

def get_wp_headers(site):
    import base64
    token = base64.b64encode(f"{site['username']}:{site['app_password']}".encode()).decode()
    return {"Authorization": f"Basic {token}"}
wp_headers = get_wp_headers(wp_site)

nl_command = st.text_area("Enter Command", placeholder="E.g., 'Create a new post titled \"How to buy property in Spain\" with content ...'")

uploaded_files = st.file_uploader("Upload Reference Files", 
                                  type=["jpg", "jpeg", "png", "csv", "xlsx", "json", "pdf", "docx", "txt"], 
                                  accept_multiple_files=True)
if uploaded_files:
    st.markdown("**Uploaded Files:**")
    for f in uploaded_files:
        st.write(f"- {f.name}")

# Optional URL for additional web scraping context
scrape_url = st.text_input("Optional: Enter a URL to scrape for extra content", "")

if st.button("Process Command"):
    if not nl_command.strip():
        st.error("Please enter a command.")
    else:
        with st.spinner("Processing command via AI..."):
            # Determine target endpoint by keywords:
            lc = nl_command.lower()
            if "listing" in lc:
                target_endpoint = "hp_listing"
            elif "page" in lc:
                target_endpoint = "pages"
            elif "delete" in lc:
                target_endpoint = "posts"  # default deletion target
            else:
                target_endpoint = "posts"
            items = fetch_items(api_base, wp_headers, target_endpoint)
            if items is None:
                st.error("Failed to fetch items from WordPress.")
                st.stop()
            extra_context = {}
            if scrape_url.strip():
                extra_context = scrape_website(scrape_url.strip())
            full_prompt = nl_command + "\nExtra context: " + json.dumps(extra_context)
            plan = process_prompt_via_openai(full_prompt, items, target_endpoint)
            st.subheader("Proposed Edits Summary")
            st.json(plan)
        if st.button("Apply These Changes"):
            results = []
            for action in plan.get("actions", []):
                if action["action"] == "create":
                    success, msg = create_item(api_base, wp_headers, target_endpoint, action)
                elif action["action"] == "update":
                    success, msg = update_item(api_base, wp_headers, target_endpoint, action)
                elif action["action"] == "delete":
                    success, msg = delete_item(api_base, wp_headers, target_endpoint, action)
                else:
                    success, msg = (False, "Unknown action")
                results.append({"ID": action.get("id"), "Action": action.get("action"), "Result": msg})
                time.sleep(0.2)
            st.subheader("Execution Log")
            st.table(pd.DataFrame(results))
            st.success("Operations completed. Review the log above.")
        else:
            st.info("Review the proposed edits above, then click 'Apply These Changes' to commit.")
