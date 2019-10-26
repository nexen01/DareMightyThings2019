from flask import Flask, escape, request, render_template, url_for
import json
import random

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

narratives = [
    'this place sucks',
    'dont buy this',
    'too bougie for you',
    'perfect property!!!'
]

@app.route('/narrative')
def narrative():
    address = escape(request.args.get('address'))
    return json.dumps({'address': address, 'narrative': random.choice(narratives)})