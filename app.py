from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(150))
  complete = db.Column(db.Boolean)

@app.route('/')

def index():
  todo_list = Todo.query.all()
  print(todo_list)
  return render_template('index.html', todo_list=todo_list)
  completed_tasks = Todo.query.filter_by(complete=True).all()
  not_completed_tasks = Todo.query.filter_by(complete=False).all()
  return render_template('index.html', completed_tasks=completed_tasks, not_completed_tasks=not_completed_tasks)

@app.route('/add', methods=['GET', 'POST'])
def add():
  title = request.form.get("title")
  new_todo = Todo(title=title, complete=False)
  db.session.add(new_todo)
  db.session.commit()
  return redirect(url_for("index"))

@app.route('/update/<int:todo_id>')
def update(todo_id):
  todo = Todo.query.filter_by(id=todo_id).first()
  todo.complete = not todo.complete
  db.session.commit()
  return redirect(url_for("index"))

@app.route('/delete/<int:todo_id>')
def delete(todo_id):
  todo = Todo.query.filter_by(id=todo_id).first()
  db.session.delete(todo)
  db.session.commit()
  return redirect(url_for("index"))

app.app_context().push()

if __name__ == '__main__':
  db.create_all()
  app.run(debug=True)