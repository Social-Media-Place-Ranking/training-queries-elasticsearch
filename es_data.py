import pandas as pd
import requests
import random
import json


def remove_duplicates(my_list):
    '''
    remove duplicates from list
    inputs: my_list: list to be cleaned from duplicates
    outputs: cleaned list
    '''
    return list(dict.fromkeys(my_list))


def extract_queries(datasets):
    '''
    extract random queries from the places names
    inputs: datasets: dataset of places
    output: quereies list
    '''
    #take the names of places and put them in a list 
    places = pd.concat(datasets)['name'].tolist()
    #remove duplicates
    unique_places = remove_duplicates(places)
    #delete places with length of string less than 3
    cleaned_places = [place for place in unique_places if len(str(place)) > 3]
    #take renadom sub parts of size 3 to 10 of the places names
    init_queries = list(map(lambda x: x[:(random.randint(3, 10))].strip(), cleaned_places))
    #remove the characters @ # %
    remove_table = str.maketrans('', '', '@#%')
    #combine the results in one dataframe
    cleaned_list = [s.translate(remove_table) for s in init_queries]
    final_queries = remove_duplicates(cleaned_list)
    return final_queries

'''
main entry point


'''
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
        #get records from elasticsearch
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


