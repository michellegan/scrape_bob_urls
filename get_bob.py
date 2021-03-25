import pandas as pd
import requests
import json
import time
from secrets import API_KEY


RADIUS = 10000 #in meters
CITIES = {'San Francisco': '37.7749,-122.4194'} #dictionary with city, lat-long string key,value pairs

def parse_result (city, result):
    try:
        arr = [city, result['name'], result['place_id'], result['types'], result['rating'], result['user_ratings_total']]
        return arr
    except:
        print("error with ", result['name'])

places_data = pd.DataFrame(columns=['city','name', 'place_id', 'types', 'avg_rating', 'num_ratings'])

for city, coord in CITIES.items():
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=' + coord + '&type=restaurant'+ '&radius=' + str(RADIUS) + '&key=' + API_KEY
    response = requests.get(url).json()
    results = response['results']
    for result in results:
        if 'rating' not in result:
            continue
        result_arr = parse_result (city, result)
        places_data.loc[len(places_data)] = result_arr
    while 'next_page_token' in response: #continue if there are still tokens left
        URL = url+  '&pagetoken=' + response['next_page_token']
        time.sleep(5)
        response = requests.get(URL).json()
        for result in response['results']:
            if 'rating' not in result:
                continue
            result_arr = parse_result(city, result)
            places_data.loc[len(places_data)] = result_arr
    
print(places_data)
