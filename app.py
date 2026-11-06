from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify)
from werkzeug.utils import secure_filename
app = Flask(__name__)

import secrets
import cs304dbi as dbi

# we need a secret_key to use flash() and sessions
app.secret_key = secrets.token_hex()

# configure DBI

# For Lookup, use 'wmdb'
# For CRUD and Ajax, use your personal db
# For project work, use your team db

print(dbi.conf('wanderw_db'))

# This gets us better error messages for certain common request errors
app.config['TRAP_BAD_REQUEST_ERRORS'] = True

@app.route('/')
def index():
    return render_template('main.html', page_title='Main Page')

@app.route('/about/')
def about():
    flash('this is a flashed message')
    return render_template('about.html', page_title='About Us')

@app.route('/createaccount/', methods = ['GET', 'POST'])
def create_account():
    if request.method == 'GET':
        return render_template('createAccount.html', page_title='Create Account')
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        if not email.endswith("@wellesley.edu"):
            flash("Must use a Wellesley Email")
            return render_template('createAccount.html', page_title='Create Account')
        else:
            with dbi.connect() as conn:
                with dbi.dict_cursor(conn) as curs:
                    curs.execute('''
                            select email from user
                            where email = %s''',
                            [email])
                    if curs.fetchall():
                        flash("There is already an account using " + email)
                        return render_template('createAccount.html', page_title='Create Account')
                    curs.execute('''INSERT INTO user(email, name)
                                    VALUES(%s, %s)''',
                                    [email, name])
                    conn.commit()
                    flash("Account created for " + email)

        return redirect(url_for('index'))

if __name__ == '__main__':
    import sys, os
    if len(sys.argv) > 1:
        # arg, if any, is the desired port number
        port = int(sys.argv[1])
        assert(port>1024)
    else:
        port = os.getuid()
    app.debug = True
    app.run('0.0.0.0',port)
