from flask import Flask, request, render_template , jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allows browser requests

# MySQL config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'   # <-- change if different
app.config['MYSQL_DB'] = 'webyweb'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# Serve your index.html
@app.route('/')
def home():
    return render_template('index.html')

# Contact API
@app.route('/api/contact', methods=['POST'])
def contact():
    try:
        data = request.get_json(force=True)
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        subject = data.get('subject', '').strip()
        message = data.get('message', '').strip()

        # Basic validation
        if not name or not email or not message:
            return jsonify({"success": False, "error": "Name, email, and message are required."}), 400

        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO messages (name, email, subject, message) VALUES (%s, %s, %s, %s)",
            (name, email, subject, message)
        )
        mysql.connection.commit()
        cur.close()

        return jsonify({"success": True, "message": "Message stored successfully!"}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# Optional: quick health check
@app.route('/health')
def health():
    return jsonify({"ok": True})

if __name__ == '__main__':
    app.run(debug=True)
  