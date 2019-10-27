from flask import Flask, escape, request, render_template, url_for
import json
import random
from urllib import parse
import pandas as pd
from subprocess import Popen, PIPE, STDOUT
import googlemaps
from datetime import datetime

print('Loading data...')

property_data = pd.read_pickle("prop_data.pkl")
availability_data = pd.read_pickle("avail_data.pkl")
place_prop_id = pd.read_pickle("place_data.pkl")

#Get rid of listings not in both lists
for i in property_data["PropertyID"]:
    if(i not in list(availability_data["PropertyID"])):
        property_data = property_data[property_data.PropertyID != i]

prop_labels = '\t'.join(property_data.columns)
avail_labels = '\t'.join(availability_data.columns)

app = Flask(__name__)

API_KEY = ""


with open('auth.json') as json_file:
    data = json.load(json_file)
    API_KEY = data['key']



gmaps = googlemaps.Client(key=API_KEY)

#airport
print("Loaded data!")

@app.route('/')
def index():
    return render_template('index.html', api_key=API_KEY)

def get_narrative(prop_id,restaurants,trains,airports,coffee_shops):
    prop_result = property_data[property_data.PropertyID == prop_id].iloc[0]
    prop_str = '\t'.join(str(val) for val in prop_result)
    avail_result = availability_data[availability_data.PropertyID == prop_id].iloc[0]
    avail_str = '\t'.join(str(val) for val in avail_result)

    bestRating = 0
    bestRestaunt = None
    for r in restaurants:
        if(r[1]>bestRating):
            bestRating = r[1]
            bestRestaunt = r

    rest_str = '\t'.join(str(val) for val in bestRestaunt)

    p = Popen(['java', '-jar', 'NarrativeGenerator.jar', prop_labels, prop_str, avail_labels, avail_str, rest_str], stdout=PIPE, stderr=STDOUT)
    output = next(p.stdout).decode('ascii')
    return output

@app.route('/narrative')
def narrative():
    prop_id = escape(request.args.get('prop_id'))
    lookup = property_data[property_data.PropertyID == prop_id]
    if (len(lookup) == 0):
        return json.dumps({
            'error': 'Invalid property ID.'
        })
    row = lookup.iloc[0]
    address = row['Address'] + ', ' + row['City'] + " " + row["State"]
    print("Narrative Request Recieved: Address=" + address + " place_id=" +prop_id)
    geocode_result = gmaps.geocode(address)
    geo = geocode_result[0]["geometry"]["location"]
    restaurants =  restaurant(address,geo)
    trains = train(address,geo)
    airports = airport(address, geo)
    coffee_shops = coffee(address, geo)
    
    if prop_id in list(property_data["PropertyID"]):
        return json.dumps({
            'narrative': get_narrative(prop_id,restaurants,trains,airports,coffee_shops),
            'prop_id': prop_id
        })
    return json.dumps({
        'error': 'Invalid property ID.'
    })

    
@app.route('/search')
def search():
    address = escape(request.args.get('address'))
    jsonString = []
    for _, row in property_data[property_data["Address"].str.contains(address, case=False)].iterrows():
        jsonString.append({
            'address': row['Address'],
            'city': row['City'],
            'state': row['State'],
            'prop_id': row['PropertyID']
        })
    return json.dumps({
        'properties': jsonString
    })






#restaurant
def restaurant(add, geo1):
    restaurants = gmaps.places_nearby(geo1, 5000, keyword = "restaurant", type = "restaurant")
    restaurant_data = []
    for restaurant in restaurants["results"]:   
        data = []
        data.append(restaurant["name"])
        data.append(restaurant["rating"])

        restaurantDict = gmaps.distance_matrix(add, restaurant['geometry']['location'], units = "imperial", mode="walking")
        distance = restaurantDict["rows"][0]["elements"][0]["distance"]["text"]
        duration = restaurantDict["rows"][0]["elements"][0]["duration"]["text"]

        data.append(distance.split()[0])

        data.append(duration)
        restaurant_data.append(data)
    return restaurant_data

#trains
def train(add, geo1):
    train_stations = gmaps.places_nearby(geo1, 10000, keyword = "train station", type = "train station")
    train_stations_data = []
    for train_station in train_stations["results"]:
        data = []
        data.append(train_station["name"])
        data.append(train_station["rating"])

        
        distanceDict = gmaps.distance_matrix(add, train_station['geometry']['location'], units = "imperial")
        distance = distanceDict["rows"][0]["elements"][0]["distance"]["text"]
        duration = distanceDict["rows"][0]["elements"][0]["duration"]["text"]
        
        data.append(distance)
        data.append(duration)
        train_stations_data.append(data)
    return train_stations_data
    
def airport(add, geo1):
    airports = gmaps.places_nearby(geo1, 100000, keyword = "airport", type = "airport")
    airport_data = []
    for airport in airports["results"]:
        data = []
        data.append(airport["name"])
        data.append(airport["rating"])

        distanceDict = gmaps.distance_matrix(add, airport['geometry']['location'], units = "imperial")
        distance = distanceDict["rows"][0]["elements"][0]["distance"]["text"]
        duration = distanceDict["rows"][0]["elements"][0]["duration"]["text"]

        data.append(distance)
        data.append(duration)
        airport_data.append(data)
    return airport_data



#coffe
def coffee(add, geo1):
    coffee_shops = gmaps.places_nearby(geo1, 5000, keyword = "coffee shop")
    coffee_shop_data = []
    for coffee_shop in coffee_shops["results"]:
        data = []
        data.append(coffee_shop["name"])
        data.append(coffee_shop["rating"])

        distanceDict = gmaps.distance_matrix(add, coffee_shop['geometry']['location'], units = "imperial", mode="walking")
        distance = distanceDict["rows"][0]["elements"][0]["distance"]["text"]
        duration = distanceDict["rows"][0]["elements"][0]["duration"]["text"]

        data.append(distance)
        data.append(duration)
        coffee_shop_data.append(data)
    return coffee_shop_data


#schools
def school(add, geo1):
    school = gmaps.places_nearby(geo1, 500, keyword = "School ", type = "School")
    school = gmaps.places_nearby(geo1, 500, keyword = "train station", type = "train station")
    school = []
    school.append(airport["results"][0]["name"])

    distanceDict = gmaps.distance_matrix(add, school[0], units = "imperial")
    distance = distanceDict["rows"][0]["elements"][0]["distance"]["text"]
    duration = distanceDict["rows"][0]["elements"][0]["duration"]["text"]
    return (school, distance)

#hotels
def hotel(add, geo1):
    hotels = gmaps.places_nearby(geo1, 1000, keyword = "hotels ", type = "hotels")
    hotels = gmaps.places_nearby(geo1, 500, keyword = "train station", type = "train station")
    hotels = []
    hotels.append(airport["results"][0]["name"])

    distanceDict = gmaps.distance_matrix(add, hotels[0], units = "imperial")
    distance = distanceDict["rows"][0]["elements"][0]["distance"]["text"]
    duration = distanceDict["rows"][0]["elements"][0]["duration"]["text"]
    return (hotels, distance)

#bus stops
def busstation(add, geo1):
    bus_station = gmaps.places_nearby(geo1, 500, keyword = "bus station ", type = "bus station")
    bus_station = gmaps.places_nearby(geo1, 500, keyword = "train station", type = "train station")
    bus_station = []
    bus_station.append(airport["results"][0]["name"])

    distanceDict = gmaps.distance_matrix(add, bus_station[0], units = "imperial")
    distance = distanceDict["rows"][0]["elements"][0]["distance"]["text"]
    duration = distanceDict["rows"][0]["elements"][0]["duration"]["text"]
    return (bus_station, distance)

#lunch
def lunch(add, geo1):
    lunch = gmaps.places_nearby(geo1, 500, keyword = "lunch ", type = "restaurant")
    lunch = gmaps.places_nearby(geo1, 500, keyword = "train station", type = "train station")
    lunch = []
    lunch.append(airport["results"][0]["name"])

    distanceDict = gmaps.distance_matrix(add, lunch[0], units = "imperial")
    distance = distanceDict["rows"][0]["elements"][0]["distance"]["text"]
    duration = distanceDict["rows"][0]["elements"][0]["duration"]["text"]
    return (lunch, distance)
