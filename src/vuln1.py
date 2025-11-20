import sqlite3
import hashlib
from flask import Flask, request




def hash_secret(secret):
    # VULNERABLE: MD5 now considered cryptographically broken
    return hashlib.md5(secret.encode()).hexdigest()
def deserialize(data):
    # VULNERABLE: Deserializing untrusted data can lead to code execution
    obj = pickle.loads(data)
    return obj
    
app = Flask(__name__)

def initialize_database():
    connection = sqlite3.connect("example.db")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'adminpass')")
    connection.commit()
    connection.close()

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    # Vulnerable to SQL injection
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    print(f"Executing query: {query}")

    connection = sqlite3.connect("example.db")
    cursor = connection.cursor()
    result = cursor.execute(query).fetchall()
    connection.close()

    if result:
        return "Login successful!"
    else:
        return "Invalid username or password"

if __name__ == "__main__":
    initialize_database()
    app.run(debug=True)
    
