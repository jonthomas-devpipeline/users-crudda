from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect("dbname='users' user='postgres' host='localhost' password='Jcmbtber1!'")
cursor = conn.cursor()

def create_all():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id SERIAL UNIQUE PRIMARY KEY,
            org_id SERIAL UNIQUE,
            first_name VARCHAR NOT NULL,
            last_name VARCHAR,
            email VARCHAR UNIQUE NOT NULL,
            phone VARCHAR,
            city VARCHAR,
            state VARCHAR (4),
            active BOOLEAN DEFAULT true
        );
    """)
    conn.commit()

create_all()

@app.route('/user/add', methods=['POST'])
def add_team():
    form = request.form
    first_name = form.get('first_name')
    if first_name == '':
        return jsonify('first_name is required!'), 400
    last_name = form.get('last_name')
    email = form.get('email')
    if email == '':
       return jsonify('email is required!')
    phone = form.get('phone')
    city = form.get('city')
    state = form.get('state')
    active = '1'
    cursor.execute('INSERT INTO users (first_name, last_name, email, phone, city, state, active) VALUES (%s, %s, %s, %s, %s, %s, %s)', (first_name, last_name, email, phone, city, state, active))
    conn.commit()
    return jsonify('User added'), 200

@app.route('/users/get')
def get_all():
    cursor.execute("SELECT * FROM users;")
    results = cursor.fetchall()

    if results:
        users = []
        for u in results:
            user_record = {
                'user_id':u[0],
                'org_id':u[1],
                'first_name':u[2],
                'last_name':u[3],
                'email':u[4],
                'phone':u[5],
                'city':u[6],
                'state': u[7],
                'active':u[8]
            }
            users.append(user_record)
        return jsonify(users), 200
    
    return 'No users found', 404

@app.route('/user/get/<user_id>')
def get_team_by_id(user_id):
    results = cursor.execute("SELECT * FROM users WHERE user_id=%s", (user_id))
    results = cursor.fetchone()
    if results:                      
        result_dictionary = {
            'user_id':results[0],
            'org_id':results[1],
            'first_name': results[2],
            'last_name': results[3],
            'email': results[4],
            'phone': results[5],
            'city': results[6],
            'state': results[7],
            'active': results[8]
        }  
        return jsonify(result_dictionary), 200
    else:
        return jsonify(f"User {user_id} Not Found")

@app.route('/user/update/<user_id>', methods=['PUT', 'PATCH', 'POST'])
def update_user(user_id):
    form = request.form
    if form.get('first_name'):
        if form.get('first_name') == '':
            return jsonify('name is required!'), 400
        if form.get('first_name').isnumeric():
            return jsonify('first name must be a string')
    if form.get('last_name'):
        if form.get('last_name').isnumeric():
            return jsonify('last name must be a string')
    if form.get('email'):
        if form.get('email').isnumeric():
            return jsonify('email must be a string')
    if form.get('phone'):
        if 10 > len(form.get('phone')) > 10:
            return jsonify('phone number must be 10 digits'), 400
    if form.get('state'):
        if form.get('state').isnumeric():
            return jsonify('state must be a two character string')
    if form.get('active'):
        if str(form.get('active')).lower() != "true":
            print()
        elif str(form.get('active')).lower() != "false":
            print()
        else:
            print(str(form.get('active')))
            return jsonify('active must be a boolean true or false'), 400 

    if form.get('first_name'):
        cursor.execute("UPDATE users SET first_name=%s WHERE user_id=%s", (form["first_name"], user_id))
        conn.commit()
    if form.get('last_name'):
        cursor.execute("UPDATE users SET last_name=%s WHERE user_id=%s", (form["last_name"], user_id))
        conn.commit()
    if form.get('email'):
        cursor.execute("UPDATE users SET email=%s WHERE user_id=%s", (form["email"], user_id))
        conn.commit()
    if form.get('phone'):
        cursor.execute("UPDATE users SET phone=%s WHERE user_id=%s", (form["phone"], user_id))
        conn.commit()
    if form.get('city'):
        cursor.execute("UPDATE users SET city=%s WHERE user_id=%s", (form["city"], user_id))
        conn.commit()
    if form.get('state'):
        cursor.execute("UPDATE users SET state=%s WHERE user_id=%s", (form["state"], user_id))
        conn.commit()
    if form.get('active'):
        cursor.execute("UPDATE users SET active=%s WHERE user_id=%s", (form["active"], user_id))
        conn.commit()   
    return jsonify('All provided fields were updated.')

@app.route('/user/delete/<user_id>', methods=['DELETE'])
def delete_team(user_id):
    cursor.execute("SELECT * FROM users WHERE user_id=%s", (user_id))
    results = cursor.fetchone()
    
    if not results:
        return (f"Team {user_id} not found."), 404

    cursor.execute("DELETE FROM users WHERE user_id=%s", (user_id))
    conn.commit()

    return (f" Team {user_id} Deleted"), 200

@app.route('/user/deactivate/<user_id>', methods=['POST', 'PATCH', 'PUT'])
def deactivate_team_by_id(user_id):
    cursor.execute("SELECT * FROM users WHERE user_id=%s", (user_id))
    results = cursor.fetchone()

    if not results:
        return (f"Team {user_id} not found."), 404
    
    cursor.execute("UPDATE users SET active=false WHERE user_id=%s;", (user_id))
    conn.commit()

    return(f"Team {user_id} Deactivated"), 200

@app.route('/user/activate/<user_id>', methods=['POST', 'PATCH', 'PUT'])
def activate_team_by_id(user_id):
    cursor.execute("SELECT * FROM users WHERE user_id=%s", (user_id))
    results = cursor.fetchone()

    if not results:
        return (f"Team {user_id} not found."), 404
    
    cursor.execute("UPDATE users SET active=true WHERE user_id=%s;", (user_id))
    conn.commit()

    return(f"Team {user_id} Activated"), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8086)
