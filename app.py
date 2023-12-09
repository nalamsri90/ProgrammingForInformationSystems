from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/tasks.db'
db = SQLAlchemy(app)
from flask_migrate import Migrate
migrate = Migrate(app, db)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    deadline = db.Column(db.DateTime)
    status = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Task {self.id}>"
    
@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([task.__dict__ for task in tasks])

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    new_task = Task(title=data['title'], description=data.get('description'), deadline=data.get('deadline'))
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'message': 'Task created successfully'})

if __name__ == "__main__":
    app.run(debug=True)