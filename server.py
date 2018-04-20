from flask import Flask, render_template, redirect, url_for, session

import config
import data_manager
import util

app = Flask(__name__)


@app.route('/')
def route_home():
    return render_template('home.html')


if __name__ == "__main__":
    app.secret_key = "AskMateGotOutOfHands"
    app.run()
