from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify)
from werkzeug.utils import secure_filename
app = Flask(__name__)

import secrets
import cs304dbi as dbi
import db

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

@app.route('/add-establishment/', methods = ["GET", "POST"])
def add_establishment():
    if request.method == "GET":
        return render_template('add-establishments.html')
    elif request.method == "POST":
        with dbi.connect() as conn:
            info = request.form
            db.add_establishment(conn, info)
            last_insert_id = db.last_insert_id(conn)['last_insert_id()']
        if info["type"] == "Hotel":
            return redirect(url_for("add_hotel", eid=last_insert_id))
        elif info["type"] == "Restaurant":
            return redirect(url_for("add_restaurant", eid=last_insert_id))
        else:
            return redirect(url_for("add_activity", eid=last_insert_id))

@app.route('/add-restaurant/<eid>', methods = ["GET", "POST"])
def add_restaurant(eid):
    with dbi.connect() as conn:
        if request.method == "GET":
            if db.get_establishment(conn, eid):
                return render_template("add-restaurant.html", eid=eid)
            else:
                flash(f'Establishment not found.')
                return redirect(url_for("index"))
        else:
            info = request.form
            db.add_restaurant(conn, eid, info)
            flash(f'Restaurant with {eid} added successfully')
            return redirect(url_for("index"))

@app.route('/add-hotel/<eid>', methods = ["GET", "POST"])
def add_hotel(eid):
    with dbi.connect() as conn:
        if request.method == "GET":
            if db.get_establishment(conn, eid):
                return render_template("add-hotel.html", eid=eid)
            else:
                flash(f'Establishment not found.')
                return redirect(url_for("index"))
        else:
            info = request.form
            db.add_hotel(conn, eid, info)
            flash(f'Hotel with {eid} added successfully')
            return redirect(url_for("index"))

@app.route('/add-activity/<eid>', methods = ["GET", "POST"])
def add_activity(eid):
    with dbi.connect() as conn:
        if request.method == "GET":
            if db.get_establishment(conn, eid):
                return render_template("add-activity.html", eid=eid)
            else:
                flash(f'Establishment not found.')
                return redirect(url_for("index"))
        else:
            info = request.form
            db.add_activity(conn, eid, info)
            flash(f'Activity with {eid} added successfully')
            return redirect(url_for("index"))

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
                if db.get_email(conn, email):
                    flash("There is already an account using " + email)
                    return render_template('createAccount.html', page_title='Create Account')
                db.add_account(conn, email, name)
                flash("Account created for " + email)

        return redirect(url_for('index'))

@app.route('/review/<eid>', methods = ['GET', 'POST'])
def add_review(eid):
    if request.method == 'GET':
        return render_template('review.html', eid = eid)
    if request.method == 'POST':
        return redirect(url_for('info', eid=eid))

@app.route('/<eid>')
def info(eid):
    with dbi.connect() as conn:
        if db.get_establishment(conn, eid):
            info = db.get_establishment_info(conn, eid)
            print(info)
            return render_template('establishment.html', establishment = info)
        else:
            flash("No establishment with that ID")
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
