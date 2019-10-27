from flask import Flask, escape, request, render_template, url_for
import json
import random
from urllib import parse
import pandas as pd
from subprocess import Popen, PIPE, STDOUT

print('Loading data...')

property_data = pd.read_pickle("prop_data.pkl")
availability_data = pd.read_pickle("avail_data.pkl")
place_prop_id = pd.read_pickle("place_data.pkl")

prop_labels = '\t'.join(property_data.columns)
avail_labels = '\t'.join(availability_data.columns)

app = Flask(__name__)

API_KEY = ""
with open('auth.json') as json_file:
    data = json.load(json_file)
    API_KEY = data['key']

print("Loaded data!")

@app.route('/')
def index():
    return render_template('index.html', api_key=API_KEY)

def get_narrative(prop_id):
    prop_result = property_data[property_data.PropertyID == prop_id].iloc[0]
    prop_str = '\t'.join(str(val) for val in prop_result)
    avail_result = availability_data[availability_data.PropertyID == prop_id].iloc[0]
    avail_str = '\t'.join(str(val) for val in avail_result)
    p = Popen(['java', '-jar', 'NarrativeGenerator.jar', prop_labels, prop_str, avail_labels, avail_str], stdout=PIPE, stderr=STDOUT)
    output = next(p.stdout).decode('ascii')
    return output

@app.route('/narrative')
def narrative():
    place_id = escape(request.args.get('place_id'))
    print(place_id)
    prop_ids = list(place_prop_id[place_prop_id.PlaceID == place_id]["PropertyID"])
    if len(prop_ids) > 0:
        prop_id = str(prop_ids[0])
        if prop_id in list(availability_data["PropertyID"]):
            return json.dumps({
                'narrative': get_narrative(prop_id),
                'prop_id': prop_id
            })
        return json.dumps({
            'error': 'No availability entry found for the property associated with this address.'
        })
    return json.dumps({
        'error': 'No properties associated with this address.'
    })
