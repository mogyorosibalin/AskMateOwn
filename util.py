from flask import session
import bcrypt

import data_manager


def get_data_from_session(label, pop=True):
    data = None
    if label in session:
        data = session[label]
        if pop:
            session.pop(label, None)
    return data


def get_dict_from_request(form_data):
    output = dict()
    for field in form_data:
        output[field] = form_data[field].strip()
    return output


def get_registration_error_messages(user):
    error_messages = list()
    if len(user["username"]) < 4:
        error_messages.append('The Username must contain at least 4 characters!')
    if len(data_manager.get_single_user_by_name(user["username"])):
        error_messages.append('This username is already in use! Please choose another one!')
    if len(user["username"]) > 20:
        error_messages.append('The Username mustn\'t contain more than 20 characters!')
    if len(user["password"]) < 8:
        error_messages.append('The Password must contain at least 8 characters!')
    if user["password"] != user["password_again"]:
        error_messages.append('The two Password must be the same!')
    return error_messages


def hash_password(plain_text_password):
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)


def get_login_error_messages(user):
    database_user = data_manager.get_single_user_by_name(user["username"])
    if database_user:
        if verify_password(user["password"], database_user[0]["password"]):
            return []
    return ['The Username and/or Password is incorrect!']


def get_new_question_error_messages(question):
    error_messages = list()
    if len(question["title"]) < 10:
        error_messages.append('The Title must contain at least 10 characters!')
    if len(question["message"]) < 20:
        error_messages.append('The Message must contain at least 20 characters!')
    return error_messages


def get_new_answer_error_messages(answer):
    if len(answer["message"]) < 10:
        return ['The answer must contain at least 10 characters!']
    return []


def get_full_single_question(user_id, question_id):
    question = data_manager.get_single_question_by_id(question_id)
    if question:
        question["comments"] = data_manager.get_all_comments_by_id(question_id, None)
        vote = data_manager.get_vote_value(user_id, question["id"], None)
        if vote:
            question["vote_value"] = vote["value"]
    return question
