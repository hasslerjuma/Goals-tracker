from flask import Flask,render_template,request,redirect,url_for
app = Flask (__name__)
goals = []

@app.route('/')
def home():
    return render_template('home.html', goals=goals)

@app.route('/add',methods=['GET','POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        goals.append({'name': name, 'category': category})
        return redirect(url_for('home'))
    return render_template('add.html')


@app.route('/delete/<int:index>')
def delete(index):
    goals.pop(index)
    return redirect(url_for('home'))


@app.route('/edit/<int:index>', methods=['GET', 'POST'])
def edit(index):
    if request.method == 'POST':
        goals[index]['name'] = request.form['name']
        goals[index]['category'] = request.form['category']
        return redirect(url_for('home'))
    return render_template('edit.html', goal=goals[index])



if __name__ == '__main__':
    app.run(debug=True)