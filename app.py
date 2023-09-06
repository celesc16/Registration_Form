from flask import Flask, request, jsonify, send_file
from psycopg2 import connect, extras  # devuelve diccionario
from cryptography.fernet import Fernet
# ejecutar y nombre de la aplicacion
app = Flask(__name__)
key = Fernet.generate_key()  # cifra datos

host = 'localhost'
port = 5432
dbname = 'userbd'
user = 'postgres'
password = 'tetecele2004'


def get_connection():
    conn = connect(host=host, port=port, dbname=dbname,
                   user=user, password=password)
    return conn
# rutas

# obtener usuario


@app.get('/api/users')
def get_users():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute('SELECT * FROM users')
    users = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify(users)


# crear usuario
@app.post('/api/users')
def create_user():
    new_user = request.get_json()
    username = new_user['username']
    surname = new_user['surname']
    age = new_user['age']
    email = new_user['email']
    password = Fernet(key).encrypt(bytes(new_user["password"], 'utf-8'))

    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute('INSERT INTO users (username,surname,age,email,password) VALUES (%s,%s,%s,%s,%s) RETURNING *',  # Retorna todo los capos
                (username, surname, age, email, password))

    new_user_create = cur.fetchone()  # extrae datos

    conn.commit()  # aplicar los cambios de la base de datos

    # asegura que no haya conexiones abiertas innecesariamente en la base de datos.
    cur.close()
    conn.close()  # aseguro que la conexión se libere y que no haya conexiones activas

    return jsonify(new_user_create)


@app.delete('/api/users/<id>')
def delete_user(id):

    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute('DELETE FROM users WHERE id = %s  RETURNING * ', (id , ))
    user = cur.fetchone()

    conn.commit()

    cur.close()
    conn.close()

    if user is None:
        return jsonify({'message': 'user not found'}), 404

    return jsonify(user)


@app.put('/api/users/<id>')
def update_user(id):

    new_user = request.get_json()
    username = new_user['username']
    surname = new_user['surname']
    age = new_user['age']
    email = new_user['email']
    password = Fernet(key).encrypt(bytes(new_user['password'], 'utf-8'))

    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute('UPDATE users SET username=%s, surname=%s, age=%s , email=%s , password=%s WHERE id=%s  RETURNING * ',
                (username, surname, age, email, password, id))

    updated_user = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    if updated_user is None:
        return jsonify({'message': 'user not found'}), 404

    return jsonify(updated_user)

# obtiene un usuario


@app.get('/api/users/<id>')
def get_user(id):

    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute('SELECT * FROM users WHERE id = %s', (id,))
    user = cur.fetchone()  # sirve para que se devuelva únicamente una sola fila

    if user is None:
        return jsonify({'message': 'user not found'}), 404

    return jsonify(user)


@app.get('/')
def home():
    return send_file('static/index.html')


# ejecutar en un puerto  si el modulo es igual a elmodulo pricipal
if __name__ == '__main__':
    app.run(debug=True)  # debug reinicia el codigo
