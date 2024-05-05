import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

direccion = os.path.abspath(os.path.dirname(__file__))#Obtenemos la dirección absoluta de donde está el archivo actual de python

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(direccion, 'database', 'tareas.db')#A la dirección absoluta se le agrega el directorio de la base de datos
db = SQLAlchemy(app)#Nos permite omitir el uso de la sintaxis específica del DBMS que estemo usando, así, podemos cambiar la base de datos a otro gestor y va a seguir funcionando

class Tareas(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    contenido = db.Column(db.String(255))
    completado = db.Column(db.Boolean)

@app.route('/')
def home():
    tareas = Tareas.query.all()
    return render_template('index.html', tareas = tareas)

@app.route('/crear-tareas', methods = ['POST'])
def create():#función para crear tareas nuevas. Da registro de contenido y completado a la base de datos
    tarea = Tareas(contenido = request.form['contenido'], completado = False)
    db.session.add(tarea)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/listo/<id>')
def listo(id):#función para cambiar el estado de completados en la base de datos. El booleano cambia a su estado opuesto
    tarea = Tareas.query.filter_by(id = int(id)).first()
    tarea.completado = not(tarea.completado)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/borrar/<id>')
def delete(id):#función para borrar registros de la base de datos
    tarea = Tareas.query.filter_by(id = int(id)).delete()
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)