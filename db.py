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
    with dbi.dict_cursor(conn) as curs:
        curs.execute('''SELECT * FROM establishment
                        WHERE city = %s AND country = %s;''', [city, country])
        return curs.fetchall()

def add_establishment(conn, info):
    with dbi.dict_cursor(conn) as curs:
        query = '''INSERT INTO establishment (name, type, website, country, city, description)
                    VALUES (%s, %s, %s, %s, %s, %s);'''
        curs.execute(query, [info['name'], info['type'], info['website'], info['country'],
                             info['city'], info['description']])
        conn.commit()

def add_restaurant(conn, eid, info):
    with dbi.dict_cursor(conn) as curs:
        query = '''INSERT INTO restaurant (eid, cuisine, reservations, outdoor_seating, credit_card, hours)
                    VALUES (%s, %s, %s, %s, %s, %s);'''
        print(eid)
        curs.execute(query, [eid, info['cuisine'], info['reservations'], info['outdoors'],
                             info['credit'], info['hours']])
        conn.commit()

def add_hotel(conn, eid, info):
    with dbi.dict_cursor(conn) as curs:
        query = '''INSERT INTO hotel (eid, gym, breakfast, pool, laundry, check_in_time, check_out_time)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)'''
        curs.execute(query, [eid, info["gym"], info["breakfast"], info["pool"], info["laundry"],
                             info["checkin"], info["checkout"]])
        conn.commit()

def add_activity(conn, eid, info):
    with dbi.dict_cursor(conn) as curs:
        query = '''INSERT INTO activity (eid, gym, breakfast, pool, laundry, check_in_time, check_out_time)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)'''
        curs.execute(query, [eid, info["gym"], info["breakfast"], info["pool"], info["laundry"],
                             info["checkin"], info["checkout"]])
        conn.commit()

def last_insert_id(conn):
    with dbi.dict_cursor(conn) as curs:
        query = '''SELECT last_insert_id()'''
        curs.execute(query)
        return curs.fetchone()

def add_account(conn, email, name):
    with dbi.dict_cursor(conn) as curs:
        curs.execute('''INSERT INTO user(email, name)
                                    VALUES(%s, %s)''',
                                    [email, name])
        conn.commit()

def get_email(conn, email):
    with dbi.dict_cursor(conn) as curs:
        curs.execute('''
                        select email from user
                        where email = %s''',
                        [email])
    return curs.fetchall()

def add_itinerary(conn, info):
    with dbi.dict_cursor(conn) as curs:
        curs.execute('''INSERT INTO itinerary(city, country, season, name, user)
                       VALUES(%s, %s, %s, %s, %s)''',
                     [info['city'], info['country'], info['season'], info['name'],
                       info['user']])
        conn.commit()
        return curs.lastrowid
        
def get_establishment_info(conn, eid):
    with dbi.dict_cursor(conn) as curs:
        curs.execute('''
                        select * from establishment
                        where eid = %s''',
                        [eid])
    return curs.fetchone()

def add_review(conn, eid, user, stars, price, body, date_visited):
    with dbi.dict_cursor(conn) as curs:
        query = '''INSERT INTO review (eid, user, stars, price,
                    review_body, date_added, date_visited)
                        VALUES (%s, %s, %s, %s, %s, CURRENT_DATE, %s)'''
        curs.execute(query, [eid, user, stars, price, body, date_visited])
        conn.commit()

def get_establishment_rating_price(conn, eid):
    with dbi.dict_cursor(conn) as curs:
        curs.execute('''
                        select AVG(stars) as r_avg, AVG(price) as p_avg 
                        from review
                        where eid = %s''',
                        [eid])
    return curs.fetchone()
    
def get_itinerary_info(conn, iid):
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
    with dbi.dict_cursor(conn) as curs:
        curs.execute('''SELECT iid, name FROM itinerary''')
        return curs.fetchall()

def add_to_itinerary(conn, iid, eid):
    with dbi.dict_cursor(conn) as curs:
        curs.execute('''INSERT INTO visit(iid, eid) VALUES (%s, %s)''',
                     [iid, eid])
        conn.commit()