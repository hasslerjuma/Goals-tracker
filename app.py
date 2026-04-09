from flask import Flask,render_template,request,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
app = Flask (__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///goals.db'
db = SQLAlchemy(app)
app.secret_key = 'your_secret_key'

class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    all_goals = Goal.query.all()
    return render_template('home.html', goals=all_goals)

@app.route('/add',methods=['GET','POST'])
def add_goal():
    if request.method == 'POST':
        new_goal = Goal(name=request.form['name'], category=request.form['category'])
        db.session.add(new_goal)
        db.session.commit()
        flash('Goal added successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('add.html')


@app.route('/delete/<int:id>')
def delete_goal(id):
    goal = Goal.query.get_or_404(id)
    db.session.delete(goal)
    db.session.commit()
    flash('Goal deleted successfully!', 'danger')
    return redirect(url_for('home'))


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_goal(id):
    goal = Goal.query.get_or_404(id)
    if request.method == 'POST':
        goal.name = request.form['name']
        goal.category = request.form['category']
        db.session.commit()
        flash('Goal updated successfully!', 'info')
        return redirect(url_for('home'))
    return render_template('edit.html', goal=goal)

@app.route('/toggle/<int:id>')
def toggle_goal(id):
    goal = Goal.query.get_or_404(id)
    goal.completed = not goal.completed
    db.session.commit()
    flash('Goal status updated!', 'info')
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)