import os, json
import geocoder
import numpy as np
import pandas as pd

# Compare two lowercased str inputs.
def compare_normalized_str(str1, str2):
    if str1 and str2:
        return str1.lower() == str2.lower()
    return True

def get(dict_obj, *path):
    element = dict_obj
    for path_element in path[:-1]:
        if path_element not in element:
            return None
        element = element.get(path_element)
    return element.get(path[-1], None)

def get_lat_long(street, city, state):
    g = geocoder.google('#{0}, ${1}, #{state}'.format(street, city, state))
    return g.latlng

def find_by_npi(source_data, npi):
    practice_data = source_data.get(npi)
    if practice_data:
        return practice_data
    raise Exception('MatchError: npi')

def match_first_name(practice_data, match_data):
    source_first_name = practice_data['doctor']['first_name']
    first_name = match_data['first_name']
    return compare_normalized_str(source_first_name, first_name)
    raise Exception('MatchError: first_name')

def match_last_name(practice_data, match_data):
    source_last_name = practice_data['doctor']['last_name']
    last_name = match_data['last_name']
    return compare_normalized_str(source_last_name, last_name)
    raise Exception('MatchError: last_name')

def match_address(practice_data, match_data):
    source_addresses = practice_data['practices']
    for address in source_addresses:
        match = compare_normalized_str(address['street'], match_data['street']) and \
                compare_normalized_str(address['street_2'], match_data['street_2']) and \
                compare_normalized_str(address['city'], match_data['city']) and \
                compare_normalized_str(address['state'], match_data['state']) and \
                match_zipcode(address['zip'], match_data['zip'])
        if match:
            return True
    raise Exception('MatchError: address')

def match_zipcode(source_zip, match_zip):
    if len(match_zip) > 5:
        return compare_normalized_str(source_zip, match_zip[:5]) or \
        compare_normalized_str(source_zip, match_zip)
    else:
        return compare_normalized_str(source_zip, match_zip)

def match_lat_long(source_addresses, street, city, state):
    lat_long = get_lat_long(street, city, state)
    if lat_long:
        source_lat_long = [ (address['lat'], address['lon']) for address in source_addresses ]
        return tuple(address_lat_long) in source_lat_long
    raise Exception('MatchError: address')
    
def try_except(fn):
    def wrapped(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            print e
    return wrapped

def get_file_path(file_name):
    abspath = os.path.abspath
    dirname = os.path.dirname
    file_path = abspath(os.path.join(dirname(dirname(__file__)), 'data', file_name))
    return file_path

@try_except
def get_json(file_name, multiple_jsons=False):
    file_path = get_file_path(file_name)
    if multiple_jsons:
        json_list  = []
        for data in open(file_path, 'r'):
            json_list.append(json.loads(data))
        return json_list
    with open(file_path, 'r') as data:
        return json.loads(data.read())

# Returns a DataFrame and Replacing nan with ''
@try_except
def get_dataframe_from_csv(file_name):
    file_path = get_file_path(file_name)
    df =  pd.read_csv(file_path)
    df = df.replace(np.nan, '', regex=True)
    return df
