from flask import Flask, render_template, redirect, url_for, session, request

import config
import data_manager
import util

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def route_home():
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def route_register():
    if request.method == 'GET':
        return render_template('register.html')


if __name__ == "__main__":
    app.secret_key = "AskMateGotOutOfHands"
    app.run()
