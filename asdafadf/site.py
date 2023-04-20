from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, Markup
import sqlite3, os, serial, time

ludi = {}

def my_factory(col,b):
    cols={}
    for i,name in enumerate(col.description):
        cols[name[0]]=b[i]
    return cols

app = Flask("ladno")

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    SECRET_KEY='development key',
))

def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = my_factory
    return rv

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    db = get_db()
    
    session['logged_in'] = False
    
    session['log'] = None
    session['password'] = None
    
    return redirect(url_for("login"))

@app.route('/registr', methods=['GET', 'POST'])
def registr():
    db = get_db()
    
    pred = ""
    
    try:
        if session['logged_in']:
            return redirect(url_for("mysite"))
    except:
            pass
    if request.method == 'POST':

        if ( len(request.form.get('log')) >= 4 and len(request.form.get('log')) <= 16 )or ( len(request.form.get('log')) >= 6 and len(request.form.get('log')) <= 12 ):
            session['logged_in'] = True
        
            session['log'] = request.form.get('log')
            session['password'] = request.form.get('password')
        

            db.execute('insert into ludi (password, log) values (?, ?)',
                    [request.form['password'], request.form['log']])
            db.commit()

            session['userId'] = db.execute('SELECT id FROM ludi WHERE log = ? AND password = ?', [request.form.get('log'), request.form.get('password')]).fetchone()["id"]
        
            return redirect(url_for("mysite"))
        else:
            pred = "login должен содержать более 3 символов и менее 17, а пароль более 7 и менее 13"
    
    return render_template('registr.html', pred=pred)

@app.route('/login', methods=['GET', 'POST'])
def login():
    db = get_db()

    pred = ""

    try:
        if session['logged_in']:
            return redirect(url_for("mysite"))
    except:
            pass
    if request.method == 'POST':
        
        cur = db.execute('SELECT log, password FROM ludi WHERE log = ? AND password = ?',
                        [request.form.get('log'), request.form.get('password')])
            
        if cur.fetchall() != []:
            session['logged_in'] = True
                
            session['log'] = request.form.get('log')
            session['password'] = request.form.get('password')
                
            session['userId'] = db.execute('SELECT id FROM ludi WHERE log = ? AND password = ?', [request.form.get('log'), request.form.get('password')]).fetchone()["id"]
            
            return redirect(url_for("mysite"))
        else:
            pred = "такого аккаунта не существует"
    
    return render_template('login.html', pred=pred)

@app.route("/mysite", methods=['GET', 'POST'])
def mysite():
    db = get_db()
    
    pred = ""

    try:
        if not session['logged_in']:
            return redirect(url_for("login"))
    except:
        return redirect(url_for("login"))
    
    if request.method == 'POST':
        if request.form.get("y") == "ydolit seba":
            return redirect(url_for("logout"))
        elif request.form.get('o') == "post":
            if request.form.get("title") != "" and len(request.form.get("text")) >= 10:
                db.execute('insert into entries (title, text, userId) values (?, ?, ?)', [request.form.get("title"), request.form.get("text"), session['userId']])
                db.commit()
            else:
                pred = "больше символов в text или название добавь"

    cur = db.execute('SELECT title, text, userId, id FROM entries order by id desc')
    #name = db.execute('select log from ludi WHERE id')
    entries = cur.fetchall()


    for i in entries:
        i['userName'] = db.execute('SELECT log FROM ludi WHERE id = ?', [i['userId'], ]).fetchone()['log']
        #i['href'] = redirect(url_for(f"show_post/{i['id']}"))

    #print(entries)
    
    
    return render_template('mysite2.html', info=f"{session['log']}", entries=entries, pred=pred)

@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    db = get_db()
    
    pred = ""
    try:
        if not session['logged_in']:
            return redirect(url_for("login"))
    except:
        return redirect(url_for("login"))
    
    if request.method == 'POST':
        if request.form.get('post') == "post":
            if len(request.form.get("text")) >= 5:
                db.execute('insert into komenti (text, userId, postId) values (?, ?, ?)', [request.form.get("text"), session['userId'], post_id])
                db.commit()

    
    cur = db.execute('SELECT title, text, userId, id FROM entries WHERE id = ?', [post_id])
    entry = cur.fetchone()
    cur = db.execute('SELECT text, postId, userId, id FROM komenti WHERE postId = ?', [post_id])
    komenti = cur.fetchall()

    for i in komenti:
        i['userName'] = db.execute('SELECT log FROM ludi WHERE id = ?', [i['userId'], ]).fetchone()['log']
    
    return render_template('stranica.html', pred=pred, entry=entry, komenti=komenti)
        
        
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

