import sqlite3

conn = sqlite3.connect('platform_storage.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL,
    company_name TEXT
)
''')

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

try:
    cursor.execute("INSERT INTO users VALUES ('admin', 'password123', 'Global Shipping Corp')")
    conn.commit()
    print("✨ SQL Database initialized successfully with an Admin account!")
except sqlite3.IntegrityError:
    print("💡 SQL Database already initialized. Skipping user injection.")

conn.close()
