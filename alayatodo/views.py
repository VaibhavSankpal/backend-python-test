from alayatodo import app
from flask import (
    g,
    redirect,
    render_template,
    request,
    session,
    jsonify
    )


@app.route('/')
def home():
    with app.open_resource('../README.md', mode='r') as f:
        readme = "".join(l for l in f)
        return render_template('index.html', readme=readme)


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_POST():
    username = request.form.get('username')
    password = request.form.get('password')

    sql = "SELECT * FROM users WHERE username = '%s' AND password = '%s'";
    cur = g.db.execute(sql % (username, password))
    user = cur.fetchone()
    if user:
        session['user'] = dict(user)
        session['logged_in'] = True
        return redirect('/todo')

    return redirect('/login')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    return redirect('/')


@app.route('/todo/<id>', methods=['GET'])
def todo(id):
    cur = g.db.execute("SELECT * FROM todos WHERE id ='%s'" % id)
    todo = cur.fetchone()
    return render_template('todo.html', todo=todo)


@app.route('/todo', methods=['GET'])
@app.route('/todo/', methods=['GET'])
def todos():
    if not session.get('logged_in'):
        return redirect('/login')
    cur = g.db.execute("SELECT * FROM todos")
    todos = cur.fetchall()
    return render_template('todos.html', todos=todos)


@app.route('/todo', methods=['POST'])
@app.route('/todo/', methods=['POST'])
def todos_POST():
    if not session.get('logged_in'):
        return redirect('/login')
    g.db.execute(
        "INSERT INTO todos (user_id, description) VALUES ('%s', '%s')"
        % (session['user']['id'], request.form.get('description', ''))
    )
    g.db.commit()
    return redirect('/todo')


@app.route('/todo/<id>', methods=['POST'])
def todo_delete(id):
    if not session.get('logged_in'):
        return redirect('/login')
    g.db.execute("DELETE FROM todos WHERE id ='%s'" % id)
    g.db.commit()
    return redirect('/todo')

@app.route('/changeStatus/<id>', methods=['POST'])
def changeStatus_POST(id):
    print("Changing status for ID "+id)
    if not session.get('logged_in'):
        return redirect('/login')
    g.db.execute(
        "UPDATE todos SET is_complete = NOT is_complete WHERE id ='%s'" % id)
    g.db.commit()
    return redirect('/todo')

@app.route('/todo/<id>/json', methods=['GET'])
def get_json_data(id):
    if not session.get('logged_in'):
        return redirect('/login')
    cur = g.db.execute("SELECT * FROM todos where id ='%s'" % id)
    todos = cur.fetchall()
    todo_as_json = []

    for row in todos:
        print(row)
        data = {
            "id":list(row)[0],
            "user_id":list(row)[1],
            "description":list(row)[2],
            "is_complete":list(row)[3]
        }
        todo_as_json.append(data)    

    print(todo_as_json)
    return jsonify(todo_as_json)

@app.route('/todo-paginated', methods=['GET'])
@app.route('/todo-paginated/<page>/<size>', methods=['GET'])
def todosPaginated(page, size):
    offset = (int(page+"") -1) * int(size+"")
    if not session.get('logged_in'):
        return redirect('/login')
    cur = g.db.execute("SELECT * FROM todos LIMIT "+size+" OFFSET "+str(offset))
    todos = cur.fetchall()
    return render_template('todos-paginated.html', todos=todos, size=size)
