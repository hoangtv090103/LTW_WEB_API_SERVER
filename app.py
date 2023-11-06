import sqlite3

from flask import Flask, jsonify, request

app = Flask(__name__)

sqldbname = 'db/website.db'


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/users', methods=['GET'])
def get_users():
    conn = sqlite3.connect(sqldbname)
    cur = conn.cursor()
    cur.execute("SELECT * FROM user")
    users = cur.fetchall()
    user_list = []
    for user in users:
        user_list.append(
            {
                'id': user[0], 'name': user[1], 'email': user[2], 'password': user[3]
            }
        )
    conn.close()
    return jsonify(user_list)


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    conn = sqlite3.connect(sqldbname)
    cur = conn.cursor()
    cur.execute("SELECT * FROM user WHERE id = ?", (user_id,))
    user = cur.fetchone()
    conn.close()
    return jsonify(
        {
            'id': user[0], 'name': user[1], 'email': user[2], 'password': user[3]
        }
    )


@app.route('/users', methods=['POST'])
def add_user():
    conn = sqlite3.connect(sqldbname)
    cur = conn.cursor()
    user_name = request.json.get('name')
    user_email = request.json.get('email')
    user_password = request.json.get('password')
    if all([user_name, user_email, user_password]):
        cur.execute("INSERT INTO user (name, email, password) VALUES (?, ?, ?)",
                    (user_name, user_email, user_password))
        conn.commit()
        conn.close()
        return jsonify(
            {
                'message': 'User added successfully'
            }
        )
    else:
        return 'Username, email and password are required', 400


@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    conn = sqlite3.connect(sqldbname)
    cur = conn.cursor()
    user_name = request.json.get('name')
    user_email = request.json.get('email')
    user_password = request.json.get('password')
    if all([user_name, user_email, user_password]):
        cur.execute("UPDATE user SET name = ?, email = ?, password = ? WHERE id = ?",
                    (user_name, user_email, user_password, user_id))
        conn.commit()
        conn.close()
        if cur.rowcount > 0:
            return jsonify(
                {
                    'message': 'User updated successfully'
                }
            )
        else:
            return 'User not found', 404
    else:
        return 'Username, email and password are required', 400


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = sqlite3.connect(sqldbname)
    cur = conn.cursor()
    cur.execute("DELETE FROM user WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    if cur.rowcount > 0:
        return jsonify(
            {
                'message': 'User deleted successfully'
            }
        )
    else:
        return 'User not found', 404


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
