from flask import Flask, escape, request
import json

app = Flask(__name__)

@app.route('/')
def index():
    return '<html><body><h1>HELLO!</h1></body></html>'

@app.route('/narrative')
def narrative():
    address = request.args.get('address')
    return json.dumps({'address': address})