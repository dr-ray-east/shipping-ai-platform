import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from google import genai
from fpdf import FPDF
import sqlite3

# Enforce uniform wide layout
st.set_page_config(page_title="AI Customs Auditor", layout="wide")

# --- MULTI-PAGE SECURE COMPLIANCE CHECKER ---
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.title("🔒 Access Denied")
    st.error("⚠️ Unauthorized entry path detected. Please authenticate on the Home landing page first.")
    st.info("💡 Open the left menu, select 'Home', and input your administrative portal credentials.")
elif st.session_state.sub_status != "Active":
    st.title("🛑 Access Suspended")
    st.error(f"⚠️ The AI Auditor is locked for {st.session_state.company} due to a pending monthly invoice.")
    st.warning("💳 Please navigate to the Home page to process your secure corporate Stripe payment.")
else:
    # --- RENDER PREMIUM APPLICATION CONTROLS ---
    st.title("⚡ AI Shipping Compliance Auditor")
    st.markdown("---")

    # Connect to Google Cloud AI Engine safely via hidden keys
    if "GEMINI_API_KEY" in st.secrets:
        API_KEY = st.secrets["GEMINI_API_KEY"]
    else:
        API_KEY = "DEVELOPER_FALLBACK_KEY"
    ai_client = genai.Client(api_key=API_KEY)

    st.subheader("📋 Step 1: Upload Your Cargo Manifest File")
    uploaded_file = st.file_uploader("Choose a CSV file...", type=["csv"])

    if uploaded_file is not None:
        raw_df = pd.read_csv(uploaded_file)
        st.info("🔄 Raw data ingested. Running defensive cleanup pipeline...")
        
        # Data Scrubbing Pipeline
        clean_df = raw_df.dropna(subset=['Container_ID', 'Cargo_Item'])
        clean_df['Customs_Code'] = pd.to_numeric(clean_df['Customs_Code'], errors='coerce')
        clean_df = clean_df.dropna(subset=['Customs_Code'])
        clean_df['Customs_Code'] = clean_df['Customs_Code'].astype(int).astype(str)
        
        st.success("✨ Data scrubbed successfully! Corrupt lines eliminated.")

        # Sidebar Panel Performance Numbers
        st.sidebar.header("📊 Cargo Shipment Metrics")
        st.sidebar.metric(label="Total Clean Containers", value=len(clean_df))
        threat_count = len(clean_df[clean_df['Customs_Code'] == '9999'])
        st.sidebar.metric(label="Critical Security Threats", value=threat_count)

        # Split Column Graphical Grid Presentation Layout
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

        # Autonomous AI Risk Mapping Execution Flow
        st.subheader("🚨 Live Threat & Compliance Analysis")
        for index, row in clean_df.iterrows():
            c_id = str(row['Container_ID']).strip()
            cargo = str(row['Cargo_Item']).strip()
            code = str(row['Customs_Code']).strip()
            
            if code == '9999':
                st.error(f"❌ SECURITY BREACH: Container **{c_id}** flagged.")
                with st.spinner(f"🤖 AI Agent is drafting an executive compliance brief for {c_id}..."):
                    prompt = f"""
                    You are a Senior Maritime Risk Analyst and International Customs Lawyer.
                    Container ID: {c_id} | Cargo: {cargo} | Code: {code}.
                    Write a formal 4-sentence Executive Briefing:
                    Sentence 1: Detail the specific violation.
                    Sentence 2: State a realistic penalty in Lakhs or Crores of INR.
                    Sentence 3: Issue an immediate impound directive.
                    Sentence 4: Suggest an alternative route to bypass the risk. Do not use bold markdown asterisks.
                    """
                    response = ai_client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
                    ai_text = response.text
                    st.info(f"📄 **AI Generated Compliance Brief ({c_id}):**\n\n{ai_text}")
                    
                    # Log Transaction Data into SQLite Archive Tables
                    conn = sqlite3.connect('platform_storage.db')
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM audit_history WHERE container_id=?", (c_id,))
                    if not cursor.fetchone():
                        cursor.execute("INSERT INTO audit_history (container_id, cargo_item, customs_code, risk_brief) VALUES (?, ?, ?, ?)",
                                       (c_id, cargo, code, ai_text))
                        conn.commit()
                        st.toast(f"💾 Container {c_id} permanently logged into SQL Server archive.")
                    conn.close()
                    
                    # Compile PDF document buffers
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
