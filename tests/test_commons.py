import os, sys, imp
module = imp.load_source('*','./app/helpers.py')

'''
Few tests, will definitely add more test in future...
'''

def test_compare_normalized_str():
    test_input = None
    test_input1 = 'test demo pass'
    test_input2 = 'test demo fail'
    assert module.compare_normalized_str(test_input, test_input1) == True
    assert module.compare_normalized_str(test_input2, test_input) == True
    assert module.compare_normalized_str(test_input1, test_input2) == False

def test_get_dataframe_from_csv():
    test_csv_name = 'match_file.csv'
    result = module.get_dataframe_from_csv(test_csv_name)
    assert len(result) > 0

def test_get_json_multiples():
    test_json_name = 'source_data.json'
    result = module.get_json(test_json_name, multiple_jsons=True)
    assert len(result) > 0
    assert isinstance(result, list)
