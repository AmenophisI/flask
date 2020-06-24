import sqlite3
from flask import Flask, render_template, request, redirect,session

app = Flask(__name__)

app.secret_key="sunabaco"

@app.route('/')
def index():
    return "Hello World"


@app.route('/top')
def toptest():
    return "toptestだよ"


@app.route('/user/<name>')
def name(name):
    return name


@app.route('/hello/<text>')
def greet(text):
    return text + "さんこんにちは"


@app.route('/temptest')
def temptest():
    name = "Amenphis"
    age = "20"
    address = "Kagawa Flag10F"
    return render_template("index.html", tpl_name=name, tpl_age=age, tpl_address=address)


@app.route('/weather')
def weather():
    py_weather = "晴れ"
    return render_template("weather.html", tpl_weather=py_weather)


@app.route('/dbtest')
def dbtest():
    conn = sqlite3.connect('flasktest.db')
    c = conn.cursor()
    # sqlでとってくる
    c.execute("SELECT name,age,address FROM staff WHERE id=1;")
    # fetchoneで格納
    staff_info = c.fetchone()
    # spl終わり
    c.close()
    print(staff_info)
    return render_template('dbtest.html', tpl_staff_info=staff_info)


@app.route('/add', methods=['GET'])
def add_get():
    if "user_id" in session:
        return render_template('add.html')
    else:
        return redirect('/list')


@app.route('/add', methods=['POST'])
def add_post():
    # formからとってくる
    user_id_py=session['user_id'][0]
    task = request.form.get("tpl_task")
    conn = sqlite3.connect('flasktest.db')
    c = conn.cursor()
    # DBに保存する
    c.execute("INSERT INTO task VALUES(null,?,?)", (task,user_id_py))
    # DBを保存する
    conn.commit()
    conn.close()
    return redirect('/list')


@app.route('/list')
def task_list():
    if "user_id" in session:
        user_id_py=session['user_id'][0]
        conn = sqlite3.connect('flasktest.db')
        c = conn.cursor()
        c.execute('SELECT name FROM member WHERE id=?',(user_id_py,))
        user_name_py=c.fetchone()[0]
        c.execute("SELECT id,task FROM task WHERE user_id=?",(user_id_py,))
        task_list_py = []
        # 一列ずつ追加
        for row in c.fetchall():
            task_list_py.append({"tpl_id": row[0], "tpl_task": row[1]})
        c.close()
        print(task_list_py)
        return render_template("task_list.html", tpl_task_list=task_list_py,user_name=user_name_py)
    else:
        return redirect('/login')


@app.route('/edit/<int:id>')
def edit(id):
    if "user_id" in session:
        conn = sqlite3.connect('flasktest.db')
        c = conn.cursor()
        c.execute("SELECT task FROM task WHERE id = ?", (id,))
        task = c.fetchone()
        c.close()
        if task is None:
            return "タスクがないよー"
        else:
            task = task[0]
            item = {"dic_id": id, "dic_task": task}
            return render_template('edit.html', tpl_task=item)
    else:
        return redirect('/login')
    


@app.route('/edit', methods=['POST'])
def update_task():
    item_id = request.form.get("task_id")
    item_id = int(item_id)
    task = request.form.get('task_input')
    conn = sqlite3.connect('flasktest.db')
    c = conn.cursor()
    c.execute("UPDATE task SET task=? WHERE id=?", (task, item_id))
    conn.commit()
    c.close()
    return redirect('/list')
     


@app.route('/del/<int:id>')
def delete(id):
    if "user_id" in session:
        conn = sqlite3.connect('flasktest.db')
        c = conn.cursor()
        c.execute('DELETE FROM task WHERE id = ?', (id,))
        conn.commit()
        c.close()
        return redirect('/list')
    else:
        return redirect('/login')



@app.route('/regist')
def regist_get():
    return render_template("regist.html")



@app.route('/regist', methods=['POST'])
def regist_post():
    name = request.form.get('member_name')
    password = request.form.get('member_password')
    conn = sqlite3.connect('flasktest.db')
    c = conn.cursor()
    c.execute('INSERT INTO member VALUES (null,?,?)', (name, password))
    conn.commit()
    c.close()
    return "登録完了です"
    

@app.route('/login')
def login_get():
    return render_template('login.html')
    


@app.route('/login', methods=['POST'])
def login_post():
    name = request.form.get('member_name')
    password = request.form.get('member_password')
    conn = sqlite3.connect('flasktest.db')
    c = conn.cursor()
    c.execute('SELECT id FROM member WHERE name = ? AND password =?',(name, password))            
    user_id = c.fetchone()
    print(user_id)
    if user_id is None:
        return render_template('login.html')
    else:
        session["user_id"]=user_id
        return redirect('/list')

@app.route('/logout')
def logout():
    session.pop("user_id",None)
    return redirect('/login')
    


@app.errorhandler(404)
def notfound(code):
    return"404エラーです！"


if __name__ == '__main__':
    app.run(debug=True)
