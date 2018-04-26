from flask import Flask, render_template, redirect, url_for, session, request

import data_manager
import util


app = Flask(__name__)
app.secret_key = "RandomSecretKeyForTestingOnThe__Localhost"


@app.route('/')
@app.route('/home')
def route_home():
    questions = data_manager.get_all_questions()[:5]
    return render_template('home.html', questions=questions, user_logged_in=util.get_data_from_session("user", False))


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
        user = util.get_data_from_session('wrong_user')
        if user is None:
            user = {"username": ""}
        error_messages = util.get_data_from_session('error_messages')
        return render_template('login.html', user=user, error_messages=error_messages)
    elif request.method == 'POST':
        user = util.get_dict_from_request(request.form)
        error_messages = util.get_login_error_messages(user)
        if len(error_messages) == 0:
            user = data_manager.get_single_user_by_name(user["username"])[0]
            session['user'] = {"id": user["id"], "username": user["username"]}
            return redirect('/')
        else:
            session["wrong_user"] = user
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
    question = data_manager.get_single_question_by_id(question_id)
    if question:
        question[0]["comments"] = data_manager.get_all_comments_by_id(question_id, None)
        answers = data_manager.get_all_answers_for_question(question_id)
        for i in range(len(answers)):
            answers[i]["comments"] = data_manager.get_all_comments_by_id(None, answers[i]["id"])
        return render_template('question.html', question=question[0], answers=answers,
                               user_logged_in=util.get_data_from_session("user", False))
    return redirect('/list')


@app.route('/question/<question_id>/delete')
def route_delete_question(question_id=None):
    user_logged_in = util.get_data_from_session("user", False)
    question = data_manager.get_single_question_by_id(question_id)
    if len(question) == 1:
        if question[0]["user_id"] == user_logged_in["id"]:
            data_manager.delete_question_by_id(question_id)
            data_manager.delete_answers_by_question_id(question_id)
            data_manager.delete_comments_by_id(question_id, None, None)
            return redirect('/list')
        return redirect('/question/{}'.format(question_id))
    return redirect('/list')


@app.route('/question/<question_id>/edit', methods=['GET', 'POST'])
def route_edit_question(question_id=None):
    user_logged_in = util.get_data_from_session("user", False)
    if request.method == 'GET':
        question = data_manager.get_single_question_by_id(question_id)
        if len(question) == 1:
            if question[0]["user_id"] == user_logged_in["id"]:
                error_messages = util.get_data_from_session("error_messages")
                question[0]["comments"] = data_manager.get_all_comments_by_id(question_id, None)
                answers = data_manager.get_all_answers_for_question(question_id)
                for i in range(len(answers)):
                    answers[i]["comments"] = data_manager.get_all_comments_by_id(None, answers[i]["id"])
                return render_template('question.html', question=question[0], answers=answers,
                                       error_messages=error_messages,
                                       editing_question=True, user_logged_in=user_logged_in)
            return redirect('/question/{}'.format(question_id))
        return redirect('/list')
    elif request.method == 'POST':
        question = util.get_dict_from_request(request.form)
        error_messages = util.get_new_question_error_messages(question)
        if len(error_messages) == 0:
            data_manager.edit_question(question_id, question)
            return redirect('/question/{}'.format(question_id))
        else:
            session["question"] = question
            session["error_messages"] = error_messages
            return redirect('/question/{}/edit'.format(question_id))


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def route_new_answer(question_id=None):
    user_logged_in = util.get_data_from_session("user", False)
    if request.method == 'GET':
        question = data_manager.get_single_question_by_id(question_id)
        answer = util.get_data_from_session("answer")
        if len(question) == 1:
            error_messages = util.get_data_from_session("error_messages")
            question[0]["comments"] = data_manager.get_all_comments_by_id(question_id, None)
            answers = data_manager.get_all_answers_for_question(question_id)
            for i in range(len(answers)):
                answers[i]["comments"] = data_manager.get_all_comments_by_id(None, answers[i]["id"])
            return render_template('question.html', question=question[0], answers=answers, answer=answer,
                                   error_messages=error_messages,
                                   new_answer=True, user_logged_in=user_logged_in)
        return redirect('/list')
    elif request.method == 'POST':
        answer = util.get_dict_from_request(request.form)
        error_messages = util.get_new_answer_error_messages(answer)
        if len(error_messages) == 0:
            data_manager.add_new_answer(question_id, answer, user_logged_in["id"])
            return redirect('/question/{}'.format(question_id))
        else:
            session["answer"] = answer
            session["error_messages"] = error_messages
            return redirect('/question/{}/new-answer'.format(question_id))


@app.route('/question/<question_id>/edit-answer/<answer_id>', methods=['GET', 'POST'])
def route_edit_answer(question_id=None, answer_id=None):
    user_logged_in = util.get_data_from_session("user", False)
    if request.method == 'GET':
        question = data_manager.get_single_question_by_id(question_id)
        if len(question) == 1:
            answer = data_manager.get_single_answer_by_id(answer_id)
            if len(answer) == 1:
                answer = util.get_data_from_session("answer")
                if not answer:
                    answer = data_manager.get_single_answer_by_id(answer_id)[0]
                error_messages = util.get_data_from_session("error_messages")
                question[0]["comments"] = data_manager.get_all_comments_by_id(question_id, None)
                answers = data_manager.get_all_answers_for_question(question_id)
                for i in range(len(answers)):
                    answers[i]["comments"] = data_manager.get_all_comments_by_id(None, answers[i]["id"])
                return render_template('question.html', question=question[0], answers=answers, answer=answer,
                                       error_messages=error_messages,
                                       new_answer=True, user_logged_in=user_logged_in)
            return redirect('/question/{}'.format(question_id))
        return redirect('/list')
    elif request.method == 'POST':
        answer = util.get_dict_from_request(request.form)
        error_messages = util.get_new_answer_error_messages(answer)
        if len(error_messages) == 0:
            data_manager.update_answer_by_id(answer_id, answer)
            return redirect('/question/{}'.format(question_id))
        else:
            session["answer"] = answer
            session["error_messages"] = error_messages
            return redirect('/question/{}/edit-answer/{}'.format(question_id, answer_id))


@app.route('/answer/<answer_id>/delete')
def route_delete_answer(answer_id=None):
    user_logged_in = util.get_data_from_session("user", False)
    answer = data_manager.get_single_answer_by_id(answer_id)
    if len(answer) == 1:
        question_id = answer[0]["question_id"]
        if answer[0]["user_id"] == user_logged_in["id"]:
            data_manager.delete_answer_by_id(answer_id)
            data_manager.delete_comments_by_id(None, answer_id, None)
        return redirect('/question/{}'.format(question_id))
    return redirect('/list')


@app.route('/question/<question_id>/new-comment', methods=['POST'])
def route_add_new_comment_for_question(question_id=None):
    user_logged_in = util.get_data_from_session("user", False)
    if data_manager.get_single_question_by_id(question_id):
        comment = util.get_dict_from_request(request.form)
        data_manager.add_new_comment(question_id, None, user_logged_in["id"], comment)
        return redirect('/question/{}'.format(question_id))
    return redirect('/list')


@app.route('/question/<question_id>/<answer_id>/new-comment', methods=['POST'])
def route_add_new_comment_for_answer(question_id=None, answer_id=None):
    user_logged_in = util.get_data_from_session("user", False)
    if data_manager.get_single_question_by_id(question_id):
        if data_manager.get_single_answer_by_id(answer_id):
            comment = util.get_dict_from_request(request.form)
            data_manager.add_new_comment(None, answer_id, user_logged_in["id"], comment)
        return redirect('/question/{}'.format(question_id))
    return redirect('/list')


@app.errorhandler(404)
def route_page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run()
