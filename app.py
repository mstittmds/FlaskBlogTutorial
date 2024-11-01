import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, abort

# make a Flask application object called app
app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SECRET_KEY']= 'your secret key'


# Function to open a connection to the database.db file
def get_db_connection():
    # create connection to the database
    conn = sqlite3.connect('database.db')
    
    # allows us to have name-based access to columns
    # the database connection will return rows we can access like regular Python dictionaries
    conn.row_factory = sqlite3.Row

    #return the connection object
    return conn

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn. close()

    if post is None:
        abort(404)
    return post
# use the app.route() decorator to create a Flask view function called index()
@app.route('/')
def index():
    #get a connection to the database
    conn = get_db_connection()
    #execute a query to read all posts from the posts database
    posts = conn.execute('SELECT * FROM posts').fetchall()
    #close the connection
    conn.close()
    #send the posts to the index.html to be displayed
    return render_template('index.html', posts=posts)


# route to create a post
@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash("Title is required")
        elif not content:
            flash('Content is reuqired')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?,?)', (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/<int:id>/edit/', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash("Title is required")
        elif not content:
            flash('Content is reuqired')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ? WHERE id =?', (title, content, id))
            conn.commit()
            conn.close()

            return redirect(url_for('index'))
    return render_template('edit.html', post=post)

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)

    conn = get_db_connection()

    conn.execute('DELETE from posts WHERE id = ?', (id,))

    conn.commit()
    conn.close()

    flash('"{}" was succuessfully deleted!'.format(post['title']))

    return redirect(url_for('index'))
app.run()