from flask import Flask,render_template,redirect,request
from flask_scss import Scss
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# My App
app=Flask(__name__)
Scss(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' 
db=SQLAlchemy(app)

# Data class ~ Row of data
class Mytask(db.Model):
    id =db.Column(db.Integer, primary_key=True)
    content=db.Column(db.String(100),nullable=False)
    complete=db.Column(db.Integer,default=0)
    created =db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self):
        return f"Task {self.id}"
#Routes to webpages
@app.route("/",methods=["POST","GET"])
def index():
    # Add a task
    if request.method=="POST":
        current_task=request.form['content']
        new_task=Mytask(content=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except:
         
            return "There was an issue adding your task"
    # Get all tasks    
    else:
        tasks=Mytask.query.order_by(Mytask.created).all()
        return render_template("index.html",tasks=tasks)

#Delete an item 
@app.route("/delete/<int:id>")
def delete(id:int):
    delete_task=Mytask.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    except:
        return "There was a problem deleting that task"

#Edit an item
@app.route("/edit/<int:id>",methods=["POST","GET"])
def edit(id:int):  
    edit_task=Mytask.query.get_or_404(id)
    if request.method=="POST":
        edit_task.content=request.form['content']
        try:
            db.session.commit()
            return redirect("/")
        except:
            return "There was an issue updating your task"
    else:
        return render_template("edit.html",task=edit_task)









































if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
