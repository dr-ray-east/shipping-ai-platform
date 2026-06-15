import streamlit as st
import pandas as pd
import sqlite3

# Page settings
st.set_page_config(page_title="Admin Audit Logs", layout="wide")

# --- UNBREAKABLE SECURITY ACCESS CONTROL GATE ---
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.title("🔒 Access Denied")
    st.error("⚠️ Please authenticate via the main Portal Login on the Home page first.")
    st.info("💡 Open the sidebar menu, navigate back to 'Home', and enter your secure organization credentials.")
elif st.session_state.sub_status != "Active":
    st.title("🛑 Module Suspended")
    st.error(f"⚠️ Access to Admin Audit Logs is blocked for {st.session_state.company} due to an unpaid monthly subscription balance.")
    st.warning("💳 Please return to the Home page and complete your Stripe checkout to unlock this premium panel.")
else:
    # --- ADMIN READ QUERIES EXECUTE ONLY IF ACCOUNT IS LOGGED IN & PAID ---
    st.title("🔒 Corporate Administration: Permanent Audit Logs")
    st.markdown("---")
    st.info("📂 This secure terminal pulls data directly from your platform's SQLite database to review historically flagged security breaches.")

    # Connect directly to our SQL storage engine file
    conn = sqlite3.connect('platform_storage.db')
    
    # Read all logged breaches using Pandas native SQL query reader
    query = "SELECT id, container_id, cargo_item, customs_code, timestamp, risk_brief FROM audit_history ORDER BY timestamp DESC"
    df_logs = pd.read_sql_query(query, conn)
    conn.close()
    
    if df_logs.empty:
        st.success("✅ Clean Registry: Zero permanent security violations have been logged into the SQL database.")
    else:
        # Render the metrics card row
        total_logged = len(df_logs)
        st.metric(label="Total Logged Compliance Incidents in Archive", value=total_logged, delta="- High Risk Profile")
        
        st.markdown("### 📋 Historical Threat Matrix")
        st.dataframe(df_logs[['id', 'container_id', 'cargo_item', 'customs_code', 'timestamp']], use_container_width=True)
        
        st.markdown("---")
        st.markdown("### 📄 Detailed AI Legal Brief Archives")
        
        # Interactive dropdown selection
        container_list = df_logs['container_id'].tolist()
        selected_container = st.selectbox("Select a historical container profile to view its full AI Legal Brief & Mitigation Plan:", container_list)
        
        if selected_container:
            brief_text = df_logs[df_logs['container_id'] == selected_container]['risk_brief'].values[0]
            st.warning(f"**Archived Compliance File for {selected_container}:**")
            st.write(brief_text)
