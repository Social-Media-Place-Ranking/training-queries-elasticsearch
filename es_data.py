import pandas as pd
import requests
import random
import json


def remove_duplicates(my_list):
    return list(dict.fromkeys(my_list))


def extract_queries(datasets):
    places = pd.concat(datasets)['name'].tolist()
    unique_places = remove_duplicates(places)
    cleaned_places = [place for place in unique_places if len(str(place)) > 3]
    init_queries = list(map(lambda x: x[:(random.randint(3, 10))].strip(), cleaned_places))
    remove_table = str.maketrans('', '', '@#%')
    cleaned_list = [s.translate(remove_table) for s in init_queries]
    final_queries = remove_duplicates(cleaned_list)
    return final_queries


if __name__ == '__main__':
    # Reading data
    restaurants = pd.read_csv('restaurant_point.csv', usecols=['name'])
    tourism = pd.read_csv('tourism_point.csv', usecols=['name'])
    poi = pd.read_csv('poi_point.csv', usecols=['name'])
    education = pd.read_csv('education_point.csv', usecols=['name'])
    # Extracting queries from Data
    geo_data = [restaurants, tourism, education, poi]
    queries = extract_queries(geo_data)
    # Create training dataset
    results = {}
    count = 0
    for query in queries[10000:]:
        response = requests.get(
            'https://query-manager.herokuapp.com/search?query=' + query + '&lon=40.7128&lat=74.0060')
        json_data = list(json.loads(response.text))[0:5]
        if len(json_data) > 0:
            for i in range(len(json_data)):
                [json_data[i].pop(key) for key in ["_id", "_index", "_type"]]
            results[query] = json_data
        # Writing Data to json file
        with open('es_data.json', 'w') as outfile:
            json.dump(results, outfile)
        print("==================================================================")
        print(count)
        print(query)
        print(json_data)
        print("==================================================================")
        count += 1
    print(len(results))


