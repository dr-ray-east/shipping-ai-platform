import sqlite3

conn = sqlite3.connect('platform_storage.db')
cursor = conn.cursor()

try:
    # Add a subscription status column to the users table
    cursor.execute("ALTER TABLE users ADD COLUMN subscription_status TEXT DEFAULT 'Active'")
    conn.commit()
    print("✨ SQL Database upgraded successfully with Subscription Status column!")
except sqlite3.OperationalError:
    print("💡 Column already exists. Database is up to date.")

# Let's create a simulated second company that has an expired/unpaid account for testing
try:
    cursor.execute("INSERT INTO users VALUES ('client_unpaid', 'password123', 'Expedited Logistics', 'Unpaid')")
    conn.commit()
    print("📦 Injected a test unpaid account ('client_unpaid' / 'password123') to verify our paywall gate works!")
except sqlite3.IntegrityError:
    pass

conn.close()
