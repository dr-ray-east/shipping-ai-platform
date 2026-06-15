import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from google import genai
from fpdf import FPDF
import sqlite3

# Page settings
st.set_page_config(page_title="AI Customs Auditor", layout="wide")

# --- UNBREAKABLE SECURITY & PAYWALL GATE ---
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.title("🔒 Access Denied")
    st.error("⚠️ Please authenticate via the main Portal Login on the Home page first.")
    st.info("💡 Use the sidebar navigation menu to click back to 'Home' and enter your organization credentials.")
elif st.session_state.sub_status != "Active":
    st.title("🛑 Module Suspended")
    st.error(f"⚠️ Access to the AI Auditor is blocked for {st.session_state.company} due to an unpaid monthly subscription balance.")
    st.warning("💳 Please go back to the Home page and complete your Stripe checkout to unlock this premium tool.")
else:
    # --- ALL PREMIUM TOOLS RUN ONLY IF LOGGED IN & PAID! ---
    st.title("⚡ AI Shipping Compliance Auditor")
    st.markdown("---")

    # Secure API Connection
   # Secure Cloud API Connection: Pull key safely from hidden Streamlit secrets
if "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]
else:
    API_KEY = "DEVELOPER_FALLBACK_KEY"


    st.subheader("📋 Step 1: Upload Your Cargo Manifest File")
    uploaded_file = st.file_uploader("Choose a CSV file...", type=["csv"])

    if uploaded_file is not None:
        raw_df = pd.read_csv(uploaded_file)
        st.info("🔄 Raw data ingested. Running defensive cleanup pipeline...")
        
        # Defensive Data Cleaning Pipeline
        clean_df = raw_df.dropna(subset=['Container_ID', 'Cargo_Item'])
        clean_df['Customs_Code'] = pd.to_numeric(clean_df['Customs_Code'], errors='coerce')
        clean_df = clean_df.dropna(subset=['Customs_Code'])
        clean_df['Customs_Code'] = clean_df['Customs_Code'].astype(int).astype(str)
        
        st.success("✨ Data scrubbed successfully! Corrupt lines eliminated.")

        # Sidebar KPI Metrics Panel
        st.sidebar.header("📊 Cargo Shipment Metrics")
        st.sidebar.metric(label="Total Clean Containers", value=len(clean_df))
        threat_count = len(clean_df[clean_df['Customs_Code'] == '9999'])
        st.sidebar.metric(label="Critical Security Threats", value=threat_count)

        # Main UI Columns Layout
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📊 Cleaned Data Grid")
            st.dataframe(clean_df, use_container_width=True)
        with col2:
            st.subheader("🎨 Cargo Distribution Count")
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.countplot(x='Cargo_Item', data=clean_df, palette='magma', ax=ax)
            plt.title("Cargo Distribution Count", fontsize=12, fontweight='bold')
            st.pyplot(fig)

        # Automated Alerts & Autonomous AI Report Loop
        st.subheader("🚨 Live Threat & Compliance Analysis")
        for index, row in clean_df.iterrows():
            c_id = str(row['Container_ID']).strip()
            cargo = str(row['Cargo_Item']).strip()
            code = str(row['Customs_Code']).strip()
            
            if code == '9999':
                st.error(f"❌ SECURITY BREACH: Container **{c_id}** flagged.")
                with st.spinner(f"🤖 AI Agent is drafting an executive compliance brief for {c_id}..."):
                    prompt = f"""
                    You are an elite International Maritime Customs Lawyer. 
                    Container ID: {c_id} has used an Illegal HS Code: {code} for '{cargo}'.
                    Write a formal 3-sentence corporate briefing detailing the violation and risk.
                    Do not use markdown formatting like bold asterisks.
                    """
                    response = ai_client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
                    ai_text = response.text
                    st.info(f"📄 **AI Generated Compliance Brief ({c_id}):**\n\n{ai_text}")
                    
                    # SQL Transaction Engine
                    conn = sqlite3.connect('platform_storage.db')
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM audit_history WHERE container_id=?", (c_id,))
                    if not cursor.fetchone():
                        cursor.execute("INSERT INTO audit_history (container_id, cargo_item, customs_code, risk_brief) VALUES (?, ?, ?, ?)",
                                       (c_id, cargo, code, ai_text))
                        conn.commit()
                        st.toast(f"💾 Container {c_id} permanently logged into SQL Server archive.")
                    conn.close()
                    
                    # PDF Engine
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_font("Arial", "B", 16)
                    pdf.cell(40, 10, f"OFFICIAL COMPLIANCE REPORT: {c_id}")
                    pdf.ln(15)
                    pdf.set_font("Arial", "", 12)
                    pdf.multi_cell(0, 10, f"Container ID: {c_id}\nCargo Type: {cargo}\nCustoms Breach Code: {code}\n\nLegal Brief:\n{ai_text}")
                    pdf_bytes = pdf.output()
                    
                    st.download_button(label=f"📥 Download {c_id} Legal Brief PDF", data=bytes(pdf_bytes), file_name=f"Compliance_Brief_{c_id}.pdf", mime="application/pdf")
            else:
                st.success(f"✅ Container {c_id} cleared safely.")
