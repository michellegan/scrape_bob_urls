import pandas as pd
import requests
import json
import time


RADIUS = 10000
CITIES = {'San Francisco': '37.7749,-122.4194'}

def parse_result (city, results):
    print (result['place_id'])
    arr = [city, result['name'], result['place_id'], result['types'], result['rating'], result['user_ratings_total']]
    return arr

places_data = pd.DataFrame(columns=['city','name', 'place_id', 'types', 'avg_rating', 'num_ratings'])

for city, coord in CITIES.items():
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=' + coord + '&type=restaurant'+ '&radius=' + str(RADIUS) + '&key=' + API_KEY
    response = requests.get(url).json()
    results = response['results']
    for result in results:
        if 'rating' not in result:
            continue
        result_arr = parse_result (city, results)
        places_data.loc[len(places_data)] = result_arr
    while 'next_page_token' in response: 
        URL = url+  '&pagetoken=' + response['next_page_token']
        time.sleep(5)
        response = requests.get(URL).json()
        for result in response['results']:
            if 'rating' not in result:
                continue
            result_arr = parse_result(city, results)
            places_data.loc[len(places_data)] = result_arr
    

print(places_data)
