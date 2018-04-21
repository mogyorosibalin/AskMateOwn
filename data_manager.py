import connection


@connection.connection_handler
def get_single_user(cursor, user_id):
    cursor.execute("""
        SELECT * FROM "user"
        WHERE id = %(id)s;
    """, {'id': user_id})
    return cursor.fetchall()


@connection.connection_handler
def get_single_user_by_name(cursor, username):
    cursor.execute("""
        SELECT * FROM "user"
        WHERE username = %(username)s;
    """, {'username': username})
    return cursor.fetchall()
