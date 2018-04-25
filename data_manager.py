import connection
import util


@connection.connection_handler
def get_all_user(cursor):
    cursor.execute("""
        SELECT * FROM "user"
        ORDER BY username;
    """)
    return cursor.fetchall()


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
        VALUES (%(username)s, %(password)s, date_trunc('second', now()), FALSE);
    """, {'username': user["username"], 'password': util.hash_password(user["password"])})


@connection.connection_handler
def get_all_questions(cursor):
    cursor.execute("""
        SELECT question.id, question.title, question.submission_time, question.view_number, question.vote_number, "user".username, COUNT(answer.id) AS answer_number
        FROM ((question
        INNER JOIN "user" ON question.user_id = "user".id)
        LEFT OUTER JOIN answer ON answer.question_id = question.id)
        WHERE question.deleted is FALSE
        GROUP BY question.id, "user".username
        ORDER BY question.submission_time DESC;
    """)
    return cursor.fetchall()


@connection.connection_handler
def get_single_question_by_id(cursor, question_id):
    cursor.execute("""
        SELECT question.id, question.title, question.message, question.submission_time, question.view_number, question.vote_number, "user".username, "user".id AS user_id, COUNT(answer.id) AS answer_number
        FROM ((question
        INNER JOIN "user" ON question.user_id = "user".id)
        LEFT OUTER JOIN answer ON answer.question_id = question.id)
        WHERE question.id = %(question_id)s AND question.deleted is FALSE
        GROUP BY question.id, "user".username, "user".id
        ORDER BY question.submission_time;
    """, {'question_id': question_id})
    return cursor.fetchall()


@connection.connection_handler
def get_all_answers_for_question(cursor, question_id):
    cursor.execute("""
        SELECT answer.message, answer.submission_time, "user".username, "user".id AS user_id
        FROM ((answer
        INNER JOIN question ON answer.question_id = question.id)
        INNER JOIN "user" ON answer.user_id = "user".id)
        WHERE answer.question_id = %(question_id)s
        ORDER BY answer.submission_time;
    """, {'question_id': question_id})
    return cursor.fetchall()


@connection.connection_handler
def add_new_question(cursor, question):
    cursor.execute("""
        INSERT INTO question
        (submission_time, view_number, vote_number, title, message, user_id)
        VALUES (date_trunc('second', now()), 0, 0, %(title)s, %(message)s, %(user_id)s)
        RETURNING id;
    """, {'title': question["title"], 'message': question["message"], 'user_id': question["user_id"]})
    return cursor.fetchall()


@connection.connection_handler
def delete_question_by_id(cursor, question_id):
    cursor.execute("""
        UPDATE question
        SET deleted = TRUE 
        WHERE id = %(id)s;
    """, {'id': question_id})


@connection.connection_handler
def delete_answers_by_question_id(cursor, question_id):
    cursor.execute("""
        UPDATE answer
        SET deleted = TRUE 
        WHERE question_id = %(id)s;
    """, {'id': question_id})
