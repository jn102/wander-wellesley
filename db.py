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