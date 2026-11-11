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

@app.route('/add-itinerary/', methods=["GET", "POST"])
def add_itinerary():
    if request.method == 'GET':
        return render_template('add-itinerary.html')
    elif request.method == 'POST':
        info = request.form
        with dbi.connect() as conn:
            iid = db.add_itinerary(conn, info)
        flash(f'Itinerary {info['name']} added successfully')
        return redirect(url_for("itinerary", iid=iid))

@app.route('/itinerary/<iid>', methods=["GET"])
def itinerary(iid):
    with dbi.connect() as conn:
        info, places = db.get_itinerary_info(conn, iid)
        return render_template('view-itinerary.html', itinerary=info, places=places)

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
    with dbi.connect() as conn:
        if request.method == 'GET':
            return render_template('review.html', eid = eid)
        if request.method == 'POST':
            user = 5 #Temporary: change to actual user once logins are implemented
            stars = request.form.get('rating')
            price = request.form.get('price')
            body = request.form.get('comments')
            date_visited = request.form.get('date_visited')
            db.add_review(conn, eid, user, stars, price, body, date_visited)
            return redirect(url_for('info', eid=eid))

@app.route('/establishment/<eid>')
def view_establishment(eid):
    with dbi.connect() as conn:
        if db.get_establishment(conn, eid):
            info = db.get_establishment_info(conn, eid)
            ratings = db.get_establishment_rating_price(conn, eid)
            return render_template('establishment.html', 
            establishment = info,
            ratings = ratings)
        else:
            flash("No establishment with that ID")
            return redirect(url_for('index'))

@app.route('/add-to-itinerary/<eid>', methods = ['GET', 'POST'])
def add_to_itinerary(eid):
    with dbi.connect() as conn:
        if not db.get_establishment(conn, eid):
            flash(f'No establishment with eid {eid}')
            return redirect(url_for('index'))
        if request.method == 'GET':
            itineraries = db.get_itineraries(conn)
            return render_template('add-to-itinerary.html', itineraries = itineraries, eid=eid)
        elif request.method == 'POST':
            iid = request.form['itinerary']
            db.add_to_itinerary(conn, iid, eid)
            flash('Establishment added successfully')
            return redirect(url_for('itinerary', iid=iid))

@app.route('/search/', methods=["GET", 'POST'])
def search():
    with dbi.connect() as conn:
        if request.method == 'GET':
            return render_template('search-establishments.html')
        if request.method == 'POST':
            city = request.form['city']
            country = request.form['country']
            establishments = db.get_establishments(conn, city, country)
            return render_template('search-results.html', city=city, 
                                   country=country, establishments=establishments)
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
