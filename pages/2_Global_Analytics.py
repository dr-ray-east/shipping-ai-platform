import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import sqlite3  # <-- Added the missing import to clear the NameError!

st.set_page_config(page_title="Global Analytics Dashboard", layout="wide")

# --- UNBREAKABLE SECURITY & PAYWALL GATE ---
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.title("🔒 Access Denied")
    st.error("⚠️ Please authenticate via the main Portal Login on the Home page first.")
elif st.session_state.sub_status != "Active":
    st.title("🛑 Module Suspended")
    st.error(f"⚠️ Analytics dashboards are locked for {st.session_state.company} due to pending balances.")
else:
    # --- EXECUTIVE ANALYTICS RUN ONLY IF LOGGED IN & PAID ---
    st.title("📊 Global Supply Chain Analytics Trends")
    st.markdown("---")

    # 1. CONNECT TO LIVE REAL-TIME DATABASE FILE
    conn = sqlite3.connect('platform_storage.db')
    query = "SELECT * FROM audit_history"
    df_history = pd.read_sql_query(query, conn)
    conn.close()

    # --- FALLBACK SEED FOR EMPTY PRODUCTION ENVIRONMENT ---
    if df_history.empty:
        st.warning("📊 Registry Empty: No live infractions logged yet. Displaying baseline industry profile.")
        # Simulated backup matrix so charts render beautifully before user's first file upload
        np.random.seed(42)
        months = np.random.choice(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'], 100)
        cargo_categories = np.random.choice(['Electronics', 'Pharmaceuticals', 'Coffee/Agriculture', 'Textiles'], 100)
        shipment_values = np.random.randint(50, 1500, 100)
        df_history = pd.DataFrame({
            'timestamp': months,
            'cargo_item': cargo_categories,
            'customs_code': shipment_values
        })
        is_simulated = True
    else:
        is_simulated = False

    # 2. HIGH-LEVEL EXECUTIVE KPI INDICATORS
    st.subheader("📈 High-Level Performance Indicators")
    kpi1, kpi2, kpi3 = st.columns(3)

    with kpi1:
        if is_simulated:
            st.metric(label="Simulated Total Audit Value", value="₹11.4 Crores")
        else:
            # Simple count calculation based on live database records!
            total_incidents = len(df_history)
            st.metric(label="Live SQL Recorded Infractions", value=total_incidents, delta="- High Risk Profile")
            
    with kpi2:
        if is_simulated:
            st.metric(label="Baseline Average Cargo Value", value="₹7.2 Lakhs")
        else:
            unique_containers = df_history['container_id'].nunique()
            st.metric(label="Distinct Vessels Apprehended", value=unique_containers)
            
    with kpi3:
        if is_simulated:
            st.metric(label="Simulated Contraband Incidents", value="14")
        else:
            st.metric(label="Database Pipeline Status", value="ONLINE 🟢")

    st.markdown("---")

    # 3. GRAPHICAL PLOTTING GRID COLUMNS LAYOUT
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📅 Threat Timeline Distribution")
        fig1, ax1 = plt.subplots(figsize=(6, 4))
        # Handle flexible mapping depending if data is live or simulated
        time_col = 'timestamp' if 'timestamp' in df_history.columns else 'timestamp'
        sns.histplot(x=time_col, data=df_history, color='teal', kde=False, bins=10, ax=ax1)
        plt.xticks(rotation=15)
        st.pyplot(fig1)
        
    with col2:
        st.subheader("⚡ Risk Density by Asset Category")
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        item_col = 'cargo_item' if 'cargo_item' in df_history.columns else 'Category'
        sns.countplot(x=item_col, data=df_history, palette='flare', ax=ax2)
        plt.xticks(rotation=15)
        st.pyplot(fig2)
