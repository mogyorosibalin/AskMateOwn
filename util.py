import data_manager
from flask import session


def get_data_from_session(label):
    data = None
    if label in session:
        data = session[label]
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
