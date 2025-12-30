from flask import Flask, request, jsonify, render_template
import pymysql
import google.generativeai as genai

app = Flask(__name__)

# --- GEMINI CONFIGURATION ---
genai.configure(api_key="AIzaSyCgbswAHkXII6J55em2NNFxZgP0EYNZTQk")
model = genai.GenerativeModel('gemini-2.5-flash')

# --- DATABASE CONNECTION ---
db = pymysql.connect(
    host="localhost",
    user="newuser",
    password="sarjan",
    database="weather",
    cursorclass=pymysql.cursors.DictCursor
)

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET"])
def register_page():
    return render_template("register.html")


# --- LOGIN ROUTE ---
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data:
        return jsonify({"status": "fail", "message": "No JSON received"})

    email = data.get("email")
    password = data.get("password")

    cursor = db.cursor()
    cursor.execute(
        "SELECT * FROM weatherpro WHERE email=%s AND password=%s",
        (email, password)
    )

    user = cursor.fetchone()

    if user:
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "fail"})

# --- REGISTER ROUTE (✅ FIXED) ---
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"status": "fail", "message": "Missing fields"})

    cursor = db.cursor()

    # Check if user already exists
    cursor.execute("SELECT * FROM weatherpro WHERE email=%s", (email,))
    existing_user = cursor.fetchone()

    if existing_user:
        return jsonify({"status": "fail", "message": "User already exists"})

    # Insert new user
    cursor.execute(
        "INSERT INTO weatherpro (email, password) VALUES (%s, %s)",
        (email, password)
    )
    db.commit()

    return jsonify({"status": "success", "message": "Registered successfully"})

# --- GEMINI CHAT ROUTE ---
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message")

    if not user_message:
        return jsonify({"reply": "Please send a message."})

    try:
        response = model.generate_content(user_message)
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)
