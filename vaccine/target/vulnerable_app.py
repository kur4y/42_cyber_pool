from flask import Flask, request, render_template_string
import sqlite3
import os


# colors
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
ORANGE = "\033[38;5;208m"
RESET = "\033[0m"

app = Flask(__name__)
DB_NAME = os.path.join(os.path.dirname(__file__), "vulnerable.db")

def init_db():
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
    
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # create secret and users tables
    c.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    c.execute("CREATE TABLE hidden_secrets (id INTEGER, secret_flag TEXT)")

    # populate with fake data
    c.execute("INSERT INTO users (username, password) VALUES ('admin', 'superpassword123')")
    c.execute("INSERT INTO users (username, password) VALUES ('bob', 'bob_is_great')")
    c.execute("INSERT INTO hidden_secrets (id, secret_flag) VALUES (1, 'FLAG{SQLI_MASTER}')")

    conn.commit()
    conn.close()

@app.route('/')
def index():
    return "<h1>Welcome to the Vaccine training target</h1><p>Available routes: /search (GET) and /login (POST)</p>"

# vulnerability from GET
@app.route('/search', methods=['GET'])
def search():
    user_id = request.args.get('id', '')
    if not user_id:
        return "Parameter required: ?id="

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()    

    # VULNERABLE : Direct concatenation of user input
    query = f"SELECT username FROM users WHERE id = {user_id}"

    # SECURED
    ##query = "SELECT username FROM users WHERE id = ?"

    try:
        ##c.execute(query, (user_id,))  # SECURED
        c.execute(query)                # VULNERABLE
        result = c.fetchall()
        return f"Search result for ID {user_id}: {result}"
    
    except Exception as e:
        return f"SQL Error: {e}", 500

# vulnerability from POST
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '')
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # VULNERABLE : Direct concatenation with quotes
    query = f"SELECT * FROM users WHERE username = '{username}'"

    # SECURED
    ##query = "SELECT * FROM users WHERE username = ?"

    try:
        ##c.execute(query, (username,)) # SECURED
        c.execute(query)                # VULNERABLE
        result = c.fetchall()
        if result:
            return f"Connected as: {result[0][1]}"
        else:
            return f"User not found."
    
    except Exception as e:
        return f"SQL Error: {e}", 500

if __name__ == "__main__":
    init_db()
    print(f"{CYAN}[INFO] SQLite database initialized.{RESET}")
    print(f"{CYAN}[INFO] Vulnerable server listening on{RESET} http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
