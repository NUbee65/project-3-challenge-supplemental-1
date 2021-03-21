from flask import Flask, render_template, request, jsonify
import requests
from config import gmaps_key, API_KEY

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/refreshMapTwo')
def refreshMapTwo():
    
    zip = request.args.get('zip')

    # make API call and pass the zip code to get coords
    zip_url = f'https://maps.googleapis.com/maps/api/geocode/json?key={gmaps_key}&components=postal_code:{zip}'
  
    zip_json = requests.get(zip_url).json()
    
    return jsonify(zip_json)


@app.route('/refreshMap')
def refreshMap():
    
    zip = request.args.get('zip')
    radius = request.args.get('radius')
    grocery_name = 'Giant Food'

    # make API call and pass the zip code to get coords
    zip_url = f'https://maps.googleapis.com/maps/api/geocode/json?key={gmaps_key}&components=postal_code:{zip}'
  
    zip_json = requests.get(zip_url).json()
    
    zip_lat = zip_json['results'][0]['geometry']['location']['lat']
    zip_lng = zip_json['results'][0]['geometry']['location']['lng']

    nearby_url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={zip_lat},{zip_lng}&radius={radius}&name={grocery_name}&key={gmaps_key}'

    nearby_json = requests.get(nearby_url).json()['results']

    return jsonify(nearby_json)

if __name__ == '__main__':
    app.run(debug=True)