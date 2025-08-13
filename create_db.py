import sqlite3

def create_db():
    con = sqlite3.connect(database="rms.db")
    cur = con.cursor()

    # Course table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS course(
            cid INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            duration TEXT,
            charges TEXT,
            description TEXT
        )
    """)

    # Users table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users(
            uid INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

    # Insert default admin user if none exists
    cur.execute("SELECT * FROM users WHERE username = ?", ("admin",))
    if cur.fetchone() is None:
        cur.execute("INSERT INTO users(username, password) VALUES (?, ?)", ("admin", "admin123"))

    con.commit()
    con.close()

create_db()
