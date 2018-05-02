from flask import Flask, render_template, request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
import os

app=Flask(__name__)
PEOPLE_FOLDER = os.path.join('static', 'image')
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///todo.db'
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER
db=SQLAlchemy(app)

class Todo (db.Model):
    id=db.Column(db.Integer,primary_key=True)
    text=db.Column (db.String(200))
    complete = db.Column(db.Boolean)

@app.route('/')
def index():
    incomplete = Todo.query.filter_by(complete=False).all()
    complete = Todo.query.filter_by(complete=True).all()
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'done.png')
    full_filename2 = os.path.join(app.config['UPLOAD_FOLDER'], 'plus.png')
    full_filename3 = os.path.join(app.config['UPLOAD_FOLDER'], 'trash.png')
    return render_template('index.html',incomplete=incomplete,complete=complete,user_image = full_filename,user_image2 = full_filename2,user_image3 = full_filename3)


 

@app.route('/add',methods=['POST'])
def add():
    todo=Todo(text=request.form['todoitem'],complete=False)
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/clear', methods = ['GET', 'POST'])
def clear():
        todo = Todo.query.all()
        Todo.query.delete()
        db.session.commit()
        return redirect(url_for('index'))

@app.route('/complete/<id>')
def complete(id):
    todo=Todo.query.filter_by(id=int(id)).first()
    todo.complete=True
    db.session.commit()
    return redirect(url_for('index'))

if __name__ =='__main__':
    app.run(debug=True,host='0.0.0.0')
