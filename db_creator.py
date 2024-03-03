import sqlite3

# SQL commands to create tables
create_site_details_sql = '''
CREATE TABLE IF NOT EXISTS SiteDetails (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    URL TEXT NOT NULL UNIQUE,
    SiteName TEXT,
    ServerName TEXT,
    ClassificationResult TEXT
);
'''

create_image_details_sql = '''
CREATE TABLE IF NOT EXISTS ImageDetails (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    ImageURL TEXT NOT NULL,
    EXIFResponse TEXT
);
'''

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('site_data.db')
cursor = conn.cursor()

# Execute SQL commands
cursor.execute(create_site_details_sql)
cursor.execute(create_image_details_sql)

# Commit changes and close the connection
conn.commit()
conn.close()

