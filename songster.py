from flask import Flask, render_template, request
import requests, bs4
import os

from scripts import pull_data

app = Flask(__name__, template_folder='templates')
@app.route('/', methods=['GET', 'POST'])
def songster():
    if request.method == 'POST':
        return render_template('base.html')
    else:
        return render_template('base.html')

if __name__ == "__main__":
    app.debug = True
    app.run()