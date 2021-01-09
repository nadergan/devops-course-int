from flask import Flask, redirect
from flask.globals import request
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os


app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
mysql_host = os.environ.get('MYSQL_HOST')
mysql_user = os.environ.get('MYSQL_USER')
mysql_pass = os.environ.get('MYSQL_PASS')

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{mysql_user}:{mysql_pass}@{mysql_host}/tasks'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/seed')
def seed():
    db.create_all()
    return 'Schema created!'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)   
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'     
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)
    
#####
@app.route('/update/<int:id>',  methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Unable to update db!'
    else:
        return render_template('update.html', task=task)


@app.route("/delete/<int:id>")
def delete(id):
    task = Todo.query.get_or_404(id)

    try:
        db.session.delete(task)
        db.session.commit()
        return redirect('/')
    except:
         return 'Unable to update db!'
    

if __name__== "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
