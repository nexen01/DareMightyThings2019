from flask import Flask, escape, request, render_template
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/narrative')
def narrative():
    address = escape(request.args.get('address'))
    return json.dumps({'address': address})