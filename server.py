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

if("Narrative" not in property_data.columns):
    print("Creating Narrative Columns")
    property_data['Narrative'] = ""

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

def getClosest(data):
    minDist = float(1000.0)
    closest = None
    for d in data:
        dist = float(d[2].split()[0])
       
        if(dist<minDist):
            minDist = dist
            closest = d
    return closest

def getBestRating(data):
    bestRating = 0
    best = None
    
    for d in data:
        if(d[1]>bestRating):
            bestRating = d[1]
            best = d
    return best

def get_narrative(row):
    prop_id = row['PropertyID']
    prop_result = property_data[property_data.PropertyID == prop_id].iloc[0]
    prop_str = '\t'.join(str(val) for val in prop_result)
    avail_result = availability_data[availability_data.PropertyID == prop_id].iloc[0]
    avail_str = '\t'.join(str(val) for val in avail_result)

    address = row['Address'] + ', ' + row['City'] + " " + row["State"]

    geocode_result = gmaps.geocode(address)
    geo = geocode_result[0]["geometry"]["location"]
   
    walk = 3000
    drive = 50000
    
    restaurants =  lookup(address,geo, None ,"restaurant",walk,"walking")  
    airports = lookup(address,geo, None, "airport", drive, "driving")

    rest_str = '\t'.join(str(val) for val in getBestRating(restaurants))
    airport_str = '\t'.join(str(val) for val in getClosest(airports))

    p = Popen(['java', '-jar', 'NarrativeGenerator.jar', prop_labels, prop_str, avail_labels, avail_str, rest_str , airport_str], stdout=PIPE, stderr=STDOUT)
    output = next(p.stdout).decode('ascii')
    return output
def googleData(row):

    address = row['Address'] + ', ' + row['City'] + " " + row["State"]

    geocode_result = gmaps.geocode(address)
    geo = geocode_result[0]["geometry"]["location"]
   
    walk = 3000
    drive = 50000

    data = []
    if(row["Bldg Subtype"] == "Mixed-Use" or row["Bldg Subtype"] == "Office"):
        restaurants =  lookup(address,geo, "lunch" ,"restaurant",walk,"walking")  
        airports = lookup(address,geo, None, "airport", drive, "driving")
        coffee_shops = lookup(address,geo, "coffee",None,walk,"walking")   
        hotels = lookup(address,geo, None, "lodging",walk,"walking")
        trains = lookup(address,geo, None, "train_station",walk, "walking")
        bus_stations = lookup(address,geo, None, "bus_station", walk,"walking")
        data.append(getBestRating(restaurants))
        data.append(getClosest(airports))
        data.append(getBestRating(coffee_shops))
        data.append(getBestRating(hotels))
        data.append(getClosest(trains))
        data.append(getClosest(bus_stations))

    elif(row["Bldg Subtype"] == "Creative"):
        restaurants =  lookup(address,geo, None ,"restaurant",drive/4,"driving")          
        coffee_shops = lookup(address,geo, "coffee",None,walk,"walking")
        live_music = lookup(address,geo, "live music",None,walk,"walking")
        art_gallery = lookup(address,geo, None, "art_gallery",walk,"walking")
        trains = lookup(address,geo, None, "train_station",walk, "walking")
        bus_stations = lookup(address,geo, None, "bus_station", walk,"walking")
        data.append(getBestRating(restaurants))
        data.append(getBestRating(live_music))
        data.append(getBestRating(art_gallery))
        data.append(getBestRating(coffee_shops))
        data.append(getClosest(trains))
        data.append(getClosest(bus_stations))


    elif(row["Bldg Subtype"] == "Condo"):
        restaurants =  lookup(address,geo, None ,"restaurant",drive/4,"driving")          
        gym = lookup(address,geo, None, "gym",walk, "walking")
        grocery = lookup(address,geo, None, "grocery_or_supermarket",walk, "walking")       
        movie_theater = lookup(address,geo, None, "movie_theater",walk, "walking")
        bar = lookup(address,geo, None, "bar",walk, "walking")
        shopping_mall = lookup(address,geo, None, "shopping_mall",walk, "walking")
        trains = lookup(address,geo, None, "train_station",walk, "walking")

        data.append(getClosest(gym))
        data.append(getClosest(grocery))
        data.append(getClosest(movie_theater))
        data.append(getClosest(bar))
        data.append(getClosest(shopping_mall))
        data.append(getBestRating(restaurants))
        data.append(getClosest(trains))

    jsonString = []
    for d in data:
        if(len(d)==0):
            continue
        jsonString.append({
                'name': d[0],
                'rating': d[1],
                'distance': d[2],
                'duration': d[3],
                'lng': d[4],
                'lat': d[5],
                'place_id': d[6]
            })
    return jsonString

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

    if prop_id in list(property_data["PropertyID"]):
        jsonString = []

       
        if(row["Narrative"] == ""):
            print(row["Narrative"])
            row["Narrative"] = get_narrative(row)
            print("Caching")
            property_data.to_pickle("prop_data.pkl")
        else:
            print("Already Cached")

        jsonString.append({
            'narrative': row["Narrative"],
            'prop_id': prop_id
        })
        jsonString.append(googleData(row))
        return json.dumps(jsonString)
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



#hotels
def hotel(add, geo1):
    hotels = gmaps.places_nearby(geo1, 5000, keyword = "hotels ", type = "hotels")
    hotel_data = []
    for hotel in hotels["results"]:
        data = []
        data.append(hotel["name"])
        data.append(hotel["rating"])

        distanceDict = gmaps.distance_matrix(add, hotel['geometry']['location'], units = "imperial", mode="walking")
        distance = distanceDict["rows"][0]["elements"][0]["distance"]["text"]
        duration = distanceDict["rows"][0]["elements"][0]["duration"]["text"]

        data.append(distance)
        data.append(duration)
        hotel_data.append(data)
    return hotel_data

#bus stops
def busstation(add, geo1):
    bus_stations = gmaps.places_nearby(geo1, 500, keyword = "bus station ", type = "bus station")
    bus_station_data = []
    for bus_station in bus_stations["results"]:
        data = []
        data.append(bus_station["name"])
        data.append(bus_station["rating"])

        distanceDict = gmaps.distance_matrix(add, bus_station['geometry']['location'], units = "imperial", mode="walking")
        distance = distanceDict["rows"][0]["elements"][0]["distance"]["text"]
        duration = distanceDict["rows"][0]["elements"][0]["duration"]["text"]

        data.append(distance)
        data.append(duration)
        bus_station_data.append(data)
    return bus_station_data

#lunch
def lunch(add, geo1):
    lunches = gmaps.places_nearby(geo1, 500, keyword = "lunch ", type = "restaurant")
    lunch_data = []
    for lunch in lunches["results"]:
        data = []
        data.append(lunch_data["name"])
        data.append(lunch_data["rating"])

        distanceDict = gmaps.distance_matrix(add, lunch_data['geometry']['location'], units = "imperial", mode="walking")
        distance = distanceDict["rows"][0]["elements"][0]["distance"]["text"]
        duration = distanceDict["rows"][0]["elements"][0]["duration"]["text"]

        data.append(distance)
        data.append(duration)
        lunch_data.append(data)
    return lunch_data


def lookup(add, geo1, key, type ,distance, mode):
    if(type == None and key != None):
        lms = gmaps.places_nearby(geo1, distance, keyword = key)
    elif(type != None and key == None):
        lms = gmaps.places_nearby(geo1, distance, type = type)
    else:
        lms = gmaps.places_nearby(geo1, distance, keyword = key, type=type)

    lm_data = []
    for lm in lms["results"]:
        data = []
        data.append(lm["name"])
        if("rating" in lm.keys()):
            data.append(lm["rating"])
        else:
            data.append(5)

        distanceDict = gmaps.distance_matrix(add, lm['geometry']['location'], units = "imperial", mode=mode)
        distance = distanceDict["rows"][0]["elements"][0]["distance"]["text"]
        duration = distanceDict["rows"][0]["elements"][0]["duration"]["text"]

        data.append(distance)
        data.append(duration)

        data.append(lm['geometry']['location']['lng'])
        data.append(lm['geometry']['location']['lat'])
        data.append(lm['place_id'])
        lm_data.append(data)
    return lm_data
