from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    deadline = db.Column(db.DateTime)
    status = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Task {self.id}>"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return render_template('tasks.html', tasks=tasks)

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    new_task = Task(title=data['title'], description=data.get('description'), deadline=data.get('deadline'))
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'message': 'Task created successfully'})

@app.route('/create-task', methods=['GET', 'POST'])
def create_task():
    if request.method == 'POST':
        data = request.form
        new_task = Task(title=data['title'], description=data.get('description'), deadline=data.get('deadline'))
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('get_tasks'))
    return render_template('create_task.html')

@app.route('/edit-task/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = Task.query.get(task_id)
    if request.method == 'POST':
        task.title = request.form['title']
        task.description = request.form['description']
        task.deadline = request.form['deadline']
        db.session.commit()
        return redirect(url_for('get_tasks'))
    return render_template('edit_task.html', task=task)




if __name__ == "__main__":
    app.run(debug=True)
