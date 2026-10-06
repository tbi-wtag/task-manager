from flask import Flask,request,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique = True, nullable = False)
    description = db.Column(db.String(120))

    def __repr__(self):
        return f"{self.name} - {self.description}"

with app.app_context():
    db.create_all()

@app.route('/')
def index(): 
    return render_template('index.html')

@app.route('/tasks')
def get_tasks():
    tasks = Task.query.all()

    output = []
    for task in tasks:
        task_data = {'id': task.id, 'name': task.name, 'description': task.description}

        output.append(task_data)

    return {"tasks" : output}

@app.route('/tasks/<id>')
def get_task(id):
    task = Task.query.get_or_404(id)
    return {'name': task.name, 'description': task.description}

@app.route('/tasks', methods = ['POST'])
def add_task():
    task = Task(name = request.json['name'], description = request.json['description'])
    db.session.add(task)
    db.session.commit()
    return {'id':task.id}


@app.route('/tasks/<id>', methods = ['DELETE'])
def delete_task(id):
    task = db.session.get(Task,id)
    if task is None:
        return {"error": "not found"}
    db.session.delete(task)
    db.session.commit()
    return{"Message":" Task deleted"}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)