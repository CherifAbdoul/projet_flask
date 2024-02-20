from flask import Flask, render_template, request, jsonify, redirect, url_for
import pymysql

app = Flask(__name__)

# Configuration de la base de données MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Utilisateur MySQL
app.config['MYSQL_PASSWORD'] = 'rootroot'  # Mot de passe MySQL
app.config['MYSQL_DB'] = 'todo_list'  # Base de données MySQL
# mysql = MySQL(app)

# Configuration de la base de données MySQL
#app.config['MYSQL_DATABASE_USER'] = 'root'
#app.config['MYSQL_DATABASE_PASSWORD'] = 'your_mysql_password'
#app.config['MYSQL_DATABASE_DB'] = 'rootroot'
#app.config['MYSQL_DATABASE_HOST'] = 'todo_list'

# Initialisation de l'extension MySQL
#mysql = MySQL(app)

methods=['POST', 'PUT', 'GET', 'PATCH', 'DELETE']

def get_db():
    return pymysql.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        db=app.config['MYSQL_DB'],
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/')
def index():
    # Récupération d'une connexion à la base de données && Création d'un curseur pour exécuter des requêtes SQL
    cur = get_db().cursor()
    cur.execute("SELECT * FROM tasks")
    cur.connection.commit()
    tasks = cur.fetchall()
    cur.close()
    return render_template('index.html', tasks=tasks)

# Route pour la création d'une tâche (POST)
@app.route('/tasks', methods=methods)
def create_task():
    if request.method == 'POST':
        #task_data = request.json
        task = request.form['task']
        cur = get_db().cursor()
        cur.execute("INSERT INTO tasks (task) VALUES (%s)", (task,))
        # mysql.connection.commit()
        cur.connection.commit()
        cur.close()
        #return jsonify({'message': 'Tâche créée avec succès'}), 201
        return redirect(url_for('index'))


# Route pour obtenir toutes les tâches (GET)
@app.route('/tasks', methods=methods)
def get_tasks():
    cur = get_db().cursor()
    cur.execute("SELECT * FROM tasks")
    tasks = cur.fetchall()
    cur.close()
    return render_template('index.html', tasks=tasks)


# Route pour obtenir une tâche par son ID (GET)
@app.route('/tasks/<int:id>', methods=methods)
def get_task(id):
    cur = get_db().cursor()
    cur.execute("SELECT * FROM tasks WHERE id = %s", (id,))
    task = cur.fetchone()
    cur.close()
    if task:
        return render_template('index.html', task=task)
    else:
        return jsonify({'message': 'Tâche non trouvée'}), 404


# Route pour mettre à jour une tâche (PUT)
@app.route('/edit_task/<int:id>', methods=methods)
def update_task(id):
    if request.form.get('_method') == 'PUT':
        task = request.form.get('new_task')
        if task is None:
            return jsonify({'error': 'Nouvelle tâche non spécifiée'}), 400
        cur = get_db().cursor()
        cur.execute("UPDATE tasks SET task=%s WHERE id=%s", (task, id))
        cur.connection.commit()
        cur.close()
    return redirect(url_for('index'))
    #return jsonify({'error': 'Tache non trouvee'}), 404  # Retourner une réponse JSON d'erreur si la tâche n'est pas trouvée


# Route pour supprimer une tâche (DELETE)
@app.route('/del_task/<int:id>', methods=methods)
def delete_task(id):
    if request.form.get('_method') == 'DELETE':
        cur = get_db().cursor()
        cur.execute("DELETE FROM tasks WHERE id=%s", (id,))
        cur.connection.commit()
        cur.close()
    return redirect(url_for('index'))


# Route pour mettre à jour partiellement une tâche (PATCH)
@app.route('/edit_patch/<int:id>', methods=methods)
def partially_update_task(id):
    if request.form.get('_method') == 'PATCH':
        task = request.form.get('task_patch')
        if task is None:
            return jsonify({'error': 'Nouvelle tâche non spécifiée'}), 400
        cur = get_db().cursor()
        cur.execute("UPDATE tasks SET task=%s WHERE id=%s", (task, id))
        cur.connection.commit()
        cur.close()
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)
