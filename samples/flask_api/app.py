from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB_FILE = "test.db"

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")


@app.route("/users", methods=["POST"])
def add_user():
    data = request.json
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name) VALUES (?)", (data["name"],))
        conn.commit()
    return jsonify({"message": "User added"}), 201

@app.route("/users", methods=["GET"])
def get_users():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = [{"id": row[0], "name": row[1]} for row in cursor.fetchall()]
    return jsonify(users)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
