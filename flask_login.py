#pip install Flask-Login

from flask import Flask, request, jsonify, g
from flask_property_list_backend.flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
login_manager = LoginManager(app)

# User model for Flask-Login
class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# User login endpoint
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # In a real-world application, you should hash the passwords before comparing them.
    # For simplicity, we'll just check if the credentials exist in the database.

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
    user_id = c.fetchone()
    conn.close()

    if not user_id:
        return jsonify({'error': 'Invalid credentials.'}), 401

    user = User(user_id[0])
    login_user(user)

    return jsonify({'message': 'Login successful!'}), 200

# User logout endpoint
@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logout successful!'}), 200

# Example of a protected endpoint (requires login)
@app.route('/protected', methods=['GET'])
@login_required
def protected_endpoint():
    return jsonify({'message': 'This is a protected endpoint. Only authenticated users can access it.'}), 200

# Custom error handler for 404 - Not Found
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Not found'}), 404

# Custom error handler for 500 - Internal Server Error
@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal Server Error'}), 500
