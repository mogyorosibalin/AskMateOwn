from flask import Flask, render_template, redirect, url_for, session, request

import data_manager
import util


app = Flask(__name__)
app.secret_key = "RandomSecretKeyForTestingOnThe__Localhost"


@app.route('/')
@app.route('/home')
def route_home():
    return render_template('home.html', user_logged_in=util.get_data_from_session("user", False))


@app.route('/register', methods=['GET', 'POST'])
def route_register():
    if util.get_data_from_session("user", False):
        return redirect('/')
    if request.method == 'GET':
        user = util.get_data_from_session('user')
        if user is None:
            user = {"username": ""}
        error_messages = util.get_data_from_session('error_messages')
        return render_template('register.html', user=user, error_messages=error_messages,
                               user_logged_in=util.get_data_from_session("user", False))
    elif request.method == 'POST':
        user = util.get_dict_from_request(request.form)
        error_messages = util.get_registration_error_messages(user)
        if len(error_messages) == 0:
            data_manager.add_new_user(user)
            return redirect('/')
        else:
            session["user"] = user
            session["error_messages"] = error_messages
            return redirect('/register')


@app.route('/login', methods=['GET', 'POST'])
def route_login():
    if util.get_data_from_session("user", False):
        return redirect('/')
    if request.method == 'GET':
        user = util.get_data_from_session('user')
        if user is None:
            user = {"username": ""}
        error_messages = util.get_data_from_session('error_messages')
        return render_template('login.html', user=user, error_messages=error_messages,
                               user_logged_in=util.get_data_from_session("user", False))
    elif request.method == 'POST':
        user = util.get_dict_from_request(request.form)
        error_messages = util.get_login_error_messages(user)
        if len(error_messages) == 0:
            user = data_manager.get_single_user_by_name(user["username"])[0]
            session['user'] = {"id": user["id"], "username": user["username"]}
            return redirect('/')
        else:
            session["user"] = user
            session["error_messages"] = error_messages
            return redirect('/login')


@app.route('/list-users')
def route_list_users():
    users = data_manager.get_all_user()
    return render_template('list-users.html', users=users,
                           user_logged_in=util.get_data_from_session("user", False))


@app.route('/logout')
def route_logout():
    util.get_data_from_session("user")
    return redirect('/')


@app.route('/list')
def route_list_questions():
    questions = data_manager.get_all_questions()
    return render_template('list.html', questions=questions,
                           user_logged_in=util.get_data_from_session("user", False))


@app.route('/new-question', methods=['GET', 'POST'])
def route_new_question():
    user_logged_in = util.get_data_from_session("user", False)
    if user_logged_in:
        if request.method == 'GET':
            question = util.get_data_from_session("question")
            error_messages = util.get_data_from_session("error_messages")
            return render_template('new-question.html', question=question, error_messages=error_messages,
                                   user_logged_in=user_logged_in)
        elif request.method == 'POST':
            question = util.get_dict_from_request(request.form)
            error_messages = util.get_new_question_error_messages(question)
            if len(error_messages) == 0:
                question["user_id"] = user_logged_in["id"]
                inserted_id = data_manager.add_new_question(question)[0]["id"]
                return redirect('/question/{}'.format(inserted_id))
            else:
                session["question"] = question
                session["error_messages"] = error_messages
                return redirect('/new-question')
    return redirect('/')


@app.route('/question/<question_id>')
def route_display_question(question_id=None):
    question = data_manager.get_single_question_by_id(question_id)[0]
    answers = data_manager.get_all_answers_for_question(question_id)
    return render_template('question.html', question=question, answers=answers,
                           user_logged_in=util.get_data_from_session("user", False))


if __name__ == "__main__":
    app.run()
