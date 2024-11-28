import mysql.connector
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Conectar a la base de datos
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        port=3309,
        user='root',
        password='',  # Cambia esto por tu contraseña de MySQL
        database='proyecto_final'  # Cambia esto por el nombre de tu base de datos
    )

# Ruta para la página principal (Ventana principal)
@app.route('/')
def index():
    return render_template('index.html')  # Página principal con botones para redirigir

# Ruta para el formulario de registro de usuario
@app.route('/registro_usuario', methods=['GET', 'POST'])
def registro_usuario():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        edad = request.form['edad']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO usuarios (nombre, correo, edad) VALUES (%s, %s, %s)', 
                       (nombre, correo, edad))
        conn.commit()
        cursor.close()
        conn.close()
        
        return redirect(url_for('consulta_usuarios'))  # Redirige a la consulta de usuarios
    
    return render_template('registro_usuario.html')  # Muestra el formulario

# Ruta para consultar usuarios
@app.route('/consulta_usuarios')
def consulta_usuarios():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios')
    usuarios = cursor.fetchall()  # Obtiene los usuarios de la base de datos
    cursor.close()
    conn.close()
    
    return render_template('consulta_usuarios.html', usuarios=usuarios)  # Muestra la lista de usuarios

# Ruta para eliminar un usuario
@app.route('/eliminar_usuario/<int:id>', methods=['POST'])
def eliminar_usuario(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM usuarios WHERE id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()
    
    return redirect(url_for('consulta_usuarios'))

# Ruta para modificar un usuario
@app.route('/editar_usuario/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        edad = request.form['edad']
        cursor.execute('UPDATE usuarios SET nombre = %s, correo = %s, edad = %s WHERE id = %s', 
                       (nombre, correo, edad, id))
        conn.commit()
        cursor.close()
        conn.close()
        
        return redirect(url_for('consulta_usuarios'))
    
    cursor.execute('SELECT * FROM usuarios WHERE id = %s', (id,))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return render_template('editar_usuario.html', usuario=usuario)

# Ruta para el formulario de registro de pedido
@app.route('/registro_pedido', methods=['GET', 'POST'])
def registro_pedido():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios')  # Obtiene los usuarios para el formulario
    usuarios = cursor.fetchall()
    
    if request.method == 'POST':
        usuario_id = request.form['usuario_id']
        producto = request.form['producto']
        fecha = request.form['fecha']
        
        cursor.execute('INSERT INTO pedidos (usuario_id, producto, fecha) VALUES (%s, %s, %s)', 
                       (usuario_id, producto, fecha))
        conn.commit()
        cursor.close()
        conn.close()
        
        return redirect(url_for('consulta_pedidos'))  # Redirige a la consulta de pedidos
    
    cursor.close()
    conn.close()
    
    return render_template('registro_pedido.html', usuarios=usuarios)  # Muestra el formulario de registro de pedido

# Ruta para consultar pedidos
@app.route('/consulta_pedidos')
def consulta_pedidos():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT pedidos.id, usuarios.nombre, pedidos.producto, pedidos.fecha '
                   'FROM pedidos JOIN usuarios ON pedidos.usuario_id = usuarios.id')
    pedidos = cursor.fetchall()  # Obtiene los pedidos desde la base de datos
    cursor.close()
    conn.close()
    
    return render_template('consulta_pedidos.html', pedidos=pedidos)  # Muestra los pedidos

# Ruta para eliminar un pedido
@app.route('/eliminar_pedido/<int:id>', methods=['POST'])
def eliminar_pedido(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM pedidos WHERE id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()
    
    return redirect(url_for('consulta_pedidos'))

# Ruta para modificar un pedido
@app.route('/editar_pedido/<int:id>', methods=['GET', 'POST'])
def editar_pedido(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        usuario_id = request.form['usuario_id']
        producto = request.form['producto']
        fecha = request.form['fecha']
        cursor.execute('UPDATE pedidos SET usuario_id = %s, producto = %s, fecha = %s WHERE id = %s', 
                       (usuario_id, producto, fecha, id))
        conn.commit()
        cursor.close()
        conn.close()
        
        return redirect(url_for('consulta_pedidos'))
    
    cursor.execute('SELECT * FROM pedidos WHERE id = %s', (id,))
    pedido = cursor.fetchone()
    cursor.execute('SELECT * FROM usuarios')  # Para rellenar el selector de usuarios
    usuarios = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('editar_pedido.html', pedido=pedido, usuarios=usuarios)

if __name__ == '__main__':
    app.run(debug=True)
