import connection
import util


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


@connection.connection_handler
def add_new_user(cursor, user):
    cursor.execute("""
        INSERT INTO "user"
        (username, password, register_time, deleted)
        VALUES (%(username)s, %(password)s, NOW(), FALSE);
    """, {'username': user["username"], 'password': util.hash_password(user["password"])})
    return cursor.fetchall()
