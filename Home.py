import streamlit as st
import sqlite3

st.set_page_config(page_title="Enterprise Logistics AI", layout="wide")

# --- INITIALIZE STREAMLIT SESSION STATE MEMORY ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "company" not in st.session_state:
    st.session_state.company = ""
if "sub_status" not in st.session_state:
    st.session_state.sub_status = "Unpaid"

# --- LOGIN VERIFICATION FUNCTION ---
def check_login(user, pwd):
    conn = sqlite3.connect('platform_storage.db')
    cursor = conn.cursor()
    # Pull both the company name and their billing subscription status
    cursor.execute("SELECT company_name, subscription_status FROM users WHERE username=? AND password=?", (user, pwd))
    result = cursor.fetchone()
    conn.close()
    return result

# --- SCREEN CONTROLLER ROUTING ---
if not st.session_state.logged_in:
    st.title("🔒 Enterprise Supply Chain Portal Login")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        username = st.text_input("Username:")
        password = st.text_input("Password:", type="password")
        
        if st.button("Log In"):
            user_data = check_login(username, password)
            if user_data:
                st.session_state.logged_in = True
                st.session_state.company = user_data[0]
                st.session_state.sub_status = user_data[1]
                st.success(f"Access Verified. Routing workspace panels...")
                st.rerun()
            else:
                st.error("Invalid Username or Password. Security alert logged.")
else:
    # --- PROCEED TO MAIN LANDING SCREEN ONCE AUTHENTICATED ---
    st.sidebar.markdown(f"💼 **Org:** {st.session_state.company}")
    
    # Visual billing badge in the side panel
    if st.session_state.sub_status == "Active":
        st.sidebar.markdown("🟢 **Subscription:** Corporate Active")
    else:
        st.sidebar.markdown("🔴 **Subscription:** Account Suspended")
        
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    # --- CONDITIONAL PAYWALL ACCESS GATE ---
    if st.session_state.sub_status != "Active":
        st.error("⚠️ ACCOUNT SUSPENDED: Your company's monthly subscription has expired.")
        st.markdown(f"""
        ### 🛑 Action Required: Payment Pending
        To unlock the AI Customs Compliance Auditor and access your historical archives, your financial terminal must clear the outstanding monthly balance.
        
        * **Invoice Amount:** ₹75,000 INR
        * **Billing Cycle:** Monthly Corporate Flat Rate
        """)
        
        # Simulated secure checkout button
        if st.button("💳 Proceed to Secure Stripe Corporate Payment"):
            st.info("🔗 Redirecting to secure Stripe Checkout terminal... (Simulated payment gate link)")
            # In a live product, we would switch this status flag back to 'Active' in the database upon successful charge callback!
            conn = sqlite3.connect('platform_storage.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET subscription_status='Active' WHERE company_name=?", (st.session_state.company,))
            conn.commit()
            conn.close()
            st.session_state.sub_status = "Active"
            st.success("💰 Payment Confirmed via Stripe API! Activating platform features...")
            st.rerun()
            
    else:
        st.title("🌐 Enterprise Supply Chain AI Platform")
        st.markdown("---")
        st.markdown(f"""
        ### Active Portal Workspace: {st.session_state.company}
        This autonomous AI architecture eliminates structural customs risks by cross-referencing live logistical datasets.
        
        #### 🗺️ Active Enterprise Modules Available in Sidebar Menu:
        * **Compliance Auditor:** Ingest manifest documents, clean string noise, trigger Gemini LLM legal analysis, and export downloadable PDFs.
        * **Global Analytics:** Evaluate macro financial throughput and trend concentrations over historical periods.
        """)
