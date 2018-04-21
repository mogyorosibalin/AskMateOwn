import connection


@connection.connection_handler
def get_single_user(cursor, user_id):
    cursor.execute("""
        SELECT * FROM user
        WHERE id = %(id)s;
    """, {'id': id})
    return cursor.fetchall()