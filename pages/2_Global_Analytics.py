import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Page settings
st.set_page_config(page_title="Global Analytics Dashboard", layout="wide")
st.title("📊 Global Supply Chain Analytics Trends")
st.markdown("---")

st.info("💡 This screen provides logistics executives with a bird's-eye view of macro compliance patterns and port throughput over time.")

# 1. Simulate Historical Shipments Dataset (200 rows tracking values)
np.random.seed(42)
months = np.random.choice(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'], 200)
cargo_categories = np.random.choice(['Electronics', 'Pharmaceuticals', 'Coffee/Agriculture', 'Textiles'], 200)
shipment_values = np.random.randint(50, 1500, 200) # Values in Lakhs of Rupees 
status = np.random.choice(['Cleared', 'Cleared', 'Cleared', 'Flagged Breach'], 200, p=[0.7, 0.15, 0.1, 0.05])

df_history = pd.DataFrame({
    'Month': months,
    'Category': cargo_categories,
    'Value_Lakhs': shipment_values,
    'Status': status
})

# 2. Executive KPI Cards Row Layout
st.subheader("📈 High-Level Performance Indicators")
kpi1, kpi2, kpi3 = st.columns(3)

with kpi1:
    total_val = df_history['Value_Lakhs'].sum() / 100 # Convert Lakhs to Crores
    st.metric(label="Total Throughput Value Audited", value=f"₹{round(total_val, 2)} Crores")
with kpi2:
    avg_shipment = df_history['Value_Lakhs'].mean()
    st.metric(label="Average Cargo Value per Container", value=f"₹{round(avg_shipment, 1)} Lakhs")
with kpi3:
    total_breaches = len(df_history[df_history['Status'] == 'Flagged Breach'])
    st.metric(label="Total Intercepted Contraband Violations", value=total_breaches, delta="- High Risk" if total_breaches > 0 else "0")

st.markdown("---")

# 3. Visual Charts Layout Columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("📅 Financial Value Flow by Month")
    monthly_trend = df_history.groupby('Month')['Value_Lakhs'].sum().reindex(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']).reset_index()
    
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    sns.lineplot(x='Month', y='Value_Lakhs', data=monthly_trend, marker='o', color='teal', linewidth=3, ax=ax1)
    plt.ylabel("Total Value (in Lakhs)")
    plt.title("Value Throughput Trend", fontsize=12, fontweight='bold')
    st.pyplot(fig1)

with col2:
    st.subheader("⚡ Risk Distribution by Product Category")
    breach_df = df_history[df_history['Status'] == 'Flagged Breach']
    
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    sns.countplot(x='Category', data=breach_df, palette='flare', ax=ax2)
    plt.ylabel("Number of Intercepted Breaches")
    plt.title("Threat Density by Asset Profile", fontsize=12, fontweight='bold')
    st.pyplot(fig2)
