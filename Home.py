import streamlit as st

# Configure the web page to look wide and modern
st.set_page_config(page_title="Enterprise Logistics AI", layout="wide")

# Main Header Banner
st.title("🌐 Enterprise Supply Chain AI Platform")
st.markdown("---")

# Platform Introduction
st.markdown("""
### Welcome to the Next-Generation Customs & Compliance Portal
This autonomous AI platform eliminates legal and financial risks by monitoring international cargo streams in real-time.

#### 🗺️ Available Platform Modules:
* **Compliance Auditor:** Ingest manifest spreadsheets, clean data records, and trigger autonomous LLM legal risk analysis.
* **Global Analytics:** Monitor total shipment values, track threat frequencies, and evaluate customs code performance.

*Use the sidebar navigation panel on the left to switch between modules seamlessly.*
""")

# Success Toast Message in the Sidebar
st.sidebar.success("Select a module above to begin.")
