import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1298",
    database="testdb"
)

# 
cursor = conn.cursor()

cursor.execute("DELETE FROM users;")
conn.commit()

# Here the user table is created
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    age INT
)
""")

users = [
    ("Gabriel", 25),
    ("Mikkel", 30),
    ("Younes", 22),
    ("Julie", 28),
    ("John", 35)
]

cursor.executemany("INSERT INTO users (name, age) VALUES (%s, %s)", users)
conn.commit()

cursor.execute("SELECT * FROM users;")
for row in cursor.fetchall():
    print(row)

cursor.close()
conn.close()