import random
import sqlite3
import string

from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort


def generate_key(length):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


app = Flask(__name__)
app.config['SECRET_KEY'] = generate_key(40)


@app.route("/")
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)


@app.route('/<int:post_id>')
def post(post_id):
    p = get_post(post_id)
    return render_template('post.html', post=p)


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('create.html')


@app.route('/<int:post_id>/edit', methods=('GET', 'POST'))
def edit(post_id):
    p = get_post(post_id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, post_id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=p)


@app.route('/<int:post_id>/delete', methods=('POST',))
def delete(post_id):
    p = get_post(post_id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (post_id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(p['title']))
    return redirect(url_for('index'))


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_post(post_id):
    conn = get_db_connection()
    p = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()
    if p is None:
        abort(404)
    return p
