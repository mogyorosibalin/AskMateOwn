import connection
import util


@connection.connection_handler
def get_all_user(cursor):
    cursor.execute("""
        SELECT * FROM users
        ORDER BY username;
    """)
    return cursor.fetchall()


@connection.connection_handler
def get_single_user(cursor, user_id):
    cursor.execute("""
        SELECT * FROM users
        WHERE id = %(id)s;
    """, {'id': user_id})
    return cursor.fetchall()


@connection.connection_handler
def get_single_user_by_name(cursor, username):
    cursor.execute("""
        SELECT * FROM users
        WHERE username = %(username)s;
    """, {'username': username})
    return cursor.fetchall()


@connection.connection_handler
def add_new_user(cursor, user):
    cursor.execute("""
        INSERT INTO users
        (username, password, register_time, deleted)
        VALUES (%(username)s, %(password)s, date_trunc('second', now()), FALSE);
    """, {'username': user["username"], 'password': util.hash_password(user["password"])})


@connection.connection_handler
def get_all_questions(cursor):
    cursor.execute("""
        SELECT question.id, question.title, question.submission_time, question.view_number, question.vote_number, users.username,
        (SELECT COUNT(*) FROM answer WHERE deleted = FALSE AND question_id = question.id) AS answer_number
        FROM (question
        INNER JOIN users ON question.user_id = users.id)
        WHERE question.deleted is FALSE
        GROUP BY question.id, users.username
        ORDER BY question.submission_time DESC;
    """)
    return cursor.fetchall()


# Replace count() with a (select)
@connection.connection_handler
def get_single_question_by_id(cursor, question_id):
    cursor.execute("""
        SELECT question.id, question.title, question.message, question.submission_time, question.view_number, question.vote_number, users.username, users.id AS user_id,
        (SELECT COUNT(*) FROM answer WHERE deleted = FALSE AND question_id = %(question_id)s) AS answer_number
        FROM (question
        INNER JOIN users ON question.user_id = users.id)
        WHERE question.id = %(question_id)s AND question.deleted is FALSE
        GROUP BY question.id, users.username, users.id
        ORDER BY question.submission_time;
    """, {'question_id': question_id})
    return cursor.fetchall()


@connection.connection_handler
def get_all_answers_for_question(cursor, question_id):
    cursor.execute("""
        SELECT answer.id, answer.message, answer.vote_number, answer.submission_time, users.username, users.id AS user_id
        FROM ((answer
        INNER JOIN question ON answer.question_id = question.id)
        INNER JOIN users ON answer.user_id = users.id)
        WHERE answer.question_id = %(question_id)s AND answer.deleted = FALSE
        ORDER BY answer.submission_time DESC;
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


@connection.connection_handler
def edit_question(cursor, question_id, question):
    cursor.execute("""
        UPDATE question
        SET title = %(title)s, message = %(message)s
        WHERE id = %(id)s;
    """, {'title': question["title"], 'message': question["message"], 'id': question_id})


@connection.connection_handler
def add_new_answer(cursor, question_id, answer, user_id):
    cursor.execute("""
        INSERT INTO answer
        (submission_time, vote_number, question_id, message, user_id)
        VALUES (date_trunc('second', now()), 0, %(question_id)s, %(message)s, %(user_id)s); 
    """, {'question_id': question_id, 'message': answer['message'], 'user_id': user_id})


@connection.connection_handler
def get_single_answer_by_id(cursor, answer_id):
    cursor.execute("""
        SELECT id, user_id, question_id, message
        FROM answer
        WHERE deleted = FALSE AND id = %(id)s;
    """, {'id': answer_id})
    return cursor.fetchall()


@connection.connection_handler
def delete_answer_by_id(cursor, answer_id):
    cursor.execute("""
        UPDATE answer
        SET deleted = TRUE 
        WHERE id = %(id)s;
    """, {'id': answer_id})


@connection.connection_handler
def update_answer_by_id(cursor, answer_id, answer):
    cursor.execute("""
        UPDATE answer
        SET message = %(message)s
        WHERE id = %(id)s;
    """, {'message': answer["message"], 'id': answer_id})


@connection.connection_handler
def add_new_comment(cursor, question_id, answer_id, user_id, comment):
    cursor.execute("""
        INSERT INTO comment
        (question_id, answer_id, user_id, message, submission_time, edited_count)
        VALUES (%(question_id)s, %(answer_id)s, %(user_id)s, %(message)s, date_trunc('second', now()), 0); 
    """, {'question_id': question_id, 'answer_id': answer_id, 'user_id': user_id, 'message': comment["message"]})


@connection.connection_handler
def get_all_comments_by_id(cursor, question_id, answer_id):
    cursor.execute("""
        SELECT comment.id, comment.message, comment.submission_time, comment.edited_count, users.username
        FROM comment
        INNER JOIN users ON comment.user_id = users.id
        WHERE question_id = %(question_id)s OR answer_id = %(answer_id)s
        ORDER BY comment.submission_time;
    """, {'question_id': question_id, 'answer_id': answer_id})
    return cursor.fetchall()
