import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(page_title="Admin Audit Logs", layout="wide")
st.title("🔒 Corporate Administration: Permanent Audit Logs")
st.markdown("---")

st.info("📂 This secure terminal pulls data directly from your platform's SQLite database to review historically flagged security breaches.")

# --- CHECK USER LOGIN STATUS ---
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("⚠️ Access Denied. Please authenticate via the Home Page portal first.")
else:
    # Connect directly to our SQL storage engine file
    conn = sqlite3.connect('platform_storage.db')
    
    # 1. READ ALL LOGGED BREACHES USING PANDAS NATIVE SQL QUERY READER
    query = "SELECT id, container_id, cargo_item, customs_code, timestamp, risk_brief FROM audit_history ORDER BY timestamp DESC"
    df_logs = pd.read_sql_query(query, conn)
    conn.close()
    
    if df_logs.empty:
        st.success("✅ Clean Registry: Zero permanent security violations have been logged into the SQL database.")
    else:
        # 2. RENDER THE METRICS ROW
        total_logged = len(df_logs)
        st.metric(label="Total Logged Compliance Incidents in Archive", value=total_logged, delta="- High Risk Profile")
        
        st.markdown("### 📋 Historical Threat Matrix")
        # Display the interactive grid containing all past entries
        st.dataframe(df_logs[['id', 'container_id', 'cargo_item', 'customs_code', 'timestamp']], use_container_width=True)
        
        st.markdown("---")
        st.markdown("### 📄 Detailed AI Legal Brief Archives")
        
        # 3. INTERACTIVE DROPDOWN TO SELECT AND READ INDIVIDUAL HISTORICAL AI BRIEFS
        container_list = df_logs['container_id'].tolist()
        selected_container = st.selectbox("Select a historical container profile to view its full AI Legal Brief & Mitigation Plan:", container_list)
        
        if selected_container:
            # Extract the specific text summary for the chosen container row
            brief_text = df_logs[df_logs['container_id'] == selected_container]['risk_brief'].values[0]
            st.warning(f"**Archived Compliance File for {selected_container}:**")
            st.write(brief_text)
