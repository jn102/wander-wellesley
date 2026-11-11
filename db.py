import cs304dbi as dbi

def get_establishment(conn, eid):
    '''Returns true if an establishment exists by eid.'''
    with dbi.dict_cursor(conn) as curs:
        query = '''SELECT eid FROM establishment WHERE eid=%s'''
        curs.execute(query, [eid])
        if curs.fetchone() is not None:
            return True
        else:
            return False

def get_establishments(conn, city, country):
    '''Returns all information about establishments in a particular city and country.'''
    with dbi.dict_cursor(conn) as curs:
        curs.execute('''SELECT * FROM establishment
                        WHERE city = %s AND country = %s;''', [city, country])
        return curs.fetchall()

def add_establishment(conn, info):
    '''Adds an establishment to the table. Returns its eid.'''
    with dbi.dict_cursor(conn) as curs:
        curs.execute('''INSERT INTO establishment (name, type, website, country, city, description)
                    VALUES (%s, %s, %s, %s, %s, %s);''', 
                    [info['name'], info['type'], info['website'], info['country'],
                             info['city'], info['description']])
        conn.commit()
        return curs.lastrowid

def add_restaurant(conn, eid, info):
    '''Adds a restaurant to the table.'''
    with dbi.dict_cursor(conn) as curs:
        curs.execute('''INSERT INTO restaurant (eid, cuisine, reservations, outdoor_seating, credit_card, hours)
                    VALUES (%s, %s, %s, %s, %s, %s);''', 
                    [eid, info['cuisine'], info['reservations'], info['outdoors'],
                             info['credit'], info['hours']])
        conn.commit()

def add_hotel(conn, eid, info):
    '''Adds a hotel to the table.'''
    with dbi.dict_cursor(conn) as curs:
        curs.execute('''INSERT INTO hotel (eid, gym, breakfast, pool, laundry, check_in_time, check_out_time)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)''', 
                    [eid, info["gym"], info["breakfast"], info["pool"], info["laundry"],
                             info["checkin"], info["checkout"]])
        conn.commit()

def add_activity(conn, eid, info):
    '''Adds an activity to the table.'''
    with dbi.dict_cursor(conn) as curs:
        curs.execute('''INSERT INTO activity (eid, gym, breakfast, pool, laundry, check_in_time, check_out_time)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)''', 
                    [eid, info["gym"], info["breakfast"], info["pool"], info["laundry"],
                             info["checkin"], info["checkout"]])
        conn.commit()

def add_account(conn, email, name, password):
    '''Adds an account to the table. Returns the user ID.'''
    with dbi.dict_cursor(conn) as curs:
        curs.execute('''INSERT INTO user(email, name, password_hash)
                                    VALUES(%s, %s, %s)''',
                                    [email, name, password])
        conn.commit()
        return curs.lastrowid

def validate_email(conn, email):
    '''Checks if an email is already in use with an account. Returns false if the email
        is already in use, true otherwise.'''
    with dbi.dict_cursor(conn) as curs:
        curs.execute('''select email from user
                        where email = %s''',
                        [email])
        if curs.fetchone():
            return False
        else:
            return True

def add_itinerary(conn, info):
    '''Adds an itinerary to the table. Returns its itinerary ID.'''
    with dbi.dict_cursor(conn) as curs:
        curs.execute('''INSERT INTO itinerary(city, country, season, name, user)
                       VALUES(%s, %s, %s, %s, %s)''',
                     [info['city'], info['country'], info['season'], info['name'],
                       info['user']])
        conn.commit()
        return curs.lastrowid
        
def get_establishment_info(conn, eid):
    '''Gets all information about an establishment by eid.'''
    with dbi.dict_cursor(conn) as curs:
        curs.execute('''select * from establishment
                        where eid = %s''',
                        [eid])
    return curs.fetchone()

def add_review(conn, eid, user, stars, price, body, date_visited):
    '''Adds a review to the table.'''
    with dbi.dict_cursor(conn) as curs:
        curs.execute('''INSERT INTO review (eid, user, stars, price,
                    review_body, date_added, date_visited)
                        VALUES (%s, %s, %s, %s, %s, CURRENT_DATE, %s)''', 
                        [eid, user, stars, price, body, date_visited])
        conn.commit()

def get_establishment_rating_price(conn, eid):
    '''Gets the average rating and price from the review table for 
        an establishment by eid.'''
    with dbi.dict_cursor(conn) as curs:
        curs.execute('''select AVG(stars) as r_avg, AVG(price) as p_avg 
                        from review
                        where eid = %s''',
                        [eid])
    return curs.fetchone()
    
def get_itinerary_info(conn, iid):
    '''Returns information about an itinerary (dict) and a list of places
        associated with that itinerary (dict) by iid.'''
    with dbi.dict_cursor(conn) as curs:
        curs.execute('''select * from itinerary
                        where iid = %s''',
                        [iid])
        info = curs.fetchone()
        curs.execute('''SELECT establishment.name as name, type, 
                        establishment.city as city, establishment.country as country 
                        FROM establishment
                        INNER JOIN visit USING (eid)
                        INNER JOIN itinerary USING (iid)
                        WHERE iid = %s''',
                        [iid])
        places = curs.fetchall()
        return info, places

def get_itineraries(conn):
    '''Returns iid and name for all itineraries in the database.'''
    with dbi.dict_cursor(conn) as curs:
        curs.execute('''SELECT iid, name FROM itinerary''')
        return curs.fetchall()

def add_to_itinerary(conn, iid, eid):
    '''Adds an item to an itinerary by inserting into the visit table.'''
    with dbi.dict_cursor(conn) as curs:
        curs.execute('''INSERT INTO visit(iid, eid) VALUES (%s, %s)''',
                     [iid, eid])
        conn.commit()