from flask import Flask, escape, request, render_template, url_for
import json
import random
from urllib import parse

app = Flask(__name__)

API_KEY = ""
with open('auth.json') as json_file:
    global API_KEY
    data = json.load(json_file)
    API_KEY = data['key']

MAPS_SRC_URL_BASE = "https://www.google.com/maps/embed/v1/place?key="+API_KEY+"&q="

@app.route('/')
def index():
    return render_template('index.html')

narratives = [
    'this place sucks',
    'dont buy this',
    'too bougie for you',
    'perfect property!!!!'
]

@app.route('/narrative')
def narrative():
    address = escape(request.args.get('address'))
    return json.dumps({
        'address': address,
        'narrative': random.choice(narratives),
        'maps_src_url': MAPS_SRC_URL_BASE + parse.quote(address)
    })
