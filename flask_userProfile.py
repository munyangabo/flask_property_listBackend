# User profile endpoint
@app.route('/profile', methods=['GET'])
@login_required
def user_profile():
    # You can access the current authenticated user through Flask-Login's 'current_user' object.
    user_id = current_user.id

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT id, username FROM users WHERE id = ?", (user_id,))
    user_data = c.fetchone()
    conn.close()

    if not user_data:
        return jsonify({'error': 'User not found.'}), 404

    user_dict = {
        'id': user_data[0],
        'username': user_data[1]
    }

    return jsonify(user_dict), 200
