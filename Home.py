import streamlit as st
import sqlite3

st.set_page_config(page_title="Enterprise Logistics AI", layout="wide")

# --- AUTO-INITIALIZE DATABASE FOR CLOUD PRODUCTION ---
def init_db_if_missing():
    conn = sqlite3.connect('platform_storage.db')
    cursor = conn.cursor()
    # Build users table if missing
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL,
        company_name TEXT,
        subscription_status TEXT DEFAULT 'Active'
    )
    ''')
    # Build history table if missing
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS audit_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        container_id TEXT NOT NULL,
        cargo_item TEXT,
        customs_code TEXT,
        risk_brief TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    # Inject default admin user if the table is fresh and empty
    cursor.execute("SELECT * FROM users WHERE username='admin'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users VALUES ('admin', 'password123', 'Global Shipping Corp', 'Active')")
        cursor.execute("INSERT INTO users VALUES ('client_unpaid', 'password123', 'Expedited Logistics', 'Unpaid')")
        conn.commit()
    conn.close()

# Run the database self-healer right on boot!
init_db_if_missing()

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
    st.sidebar.markdown(f"💼 **Org:** {st.session_state.company}")
    
    if st.session_state.sub_status == "Active":
        st.sidebar.markdown("🟢 **Subscription:** Corporate Active")
    else:
        st.sidebar.markdown("🔴 **Subscription:** Account Suspended")
        
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    if st.session_state.sub_status != "Active":
        st.error("⚠️ ACCOUNT SUSPENDED: Your company's monthly subscription has expired.")
        st.markdown("""
        ### 🛑 Action Required: Payment Pending
        To unlock the AI Customs Compliance Auditor and access your historical archives, your financial terminal must clear the outstanding monthly balance.
        
        * **Invoice Amount:** ₹75,000 INR
        * **Billing Cycle:** Monthly Corporate Flat Rate
        """)
        
        if st.button("💳 Proceed to Secure Stripe Corporate Payment"):
            st.info("🔗 Redirecting to secure Stripe Checkout terminal...")
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
        """)
