from flask import Flask, render_template, redirect, url_for, session, request

import data_manager
import util

app = Flask(__name__)
app.secret_key = "RandomSecretKeyForTestingOnThe__Localhost"


@app.route('/')
@app.route('/home')
def route_home():
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def route_register():
    if request.method == 'GET':
        user = util.get_data_from_session('user')
        if user is None:
            user = {"username": ""}
        error_messages = util.get_data_from_session('error_messages')
        return render_template('register.html', user=user, error_messages=error_messages)
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
    if request.method == 'GET':
        user = util.get_data_from_session('user')
        if user is None:
            user = {"username": ""}
        error_messages = util.get_data_from_session('error_messages')
        return render_template('login.html', user=user, error_messages=error_messages)
    elif request.method == 'POST':
        user = util.get_dict_from_request(request.form)
        error_messages = util.get_login_error_messages(user)
        if len(error_messages) == 0:
            session['username'] = user["username"]
            return redirect('/')
        else:
            session["user"] = user
            session["error_messages"] = error_messages
            return redirect('/login')


@app.route('/list-users')
def route_list_users():
    users = data_manager.get_all_user()
    return render_template('list-users.html', users=users)


if __name__ == "__main__":
    app.run()
