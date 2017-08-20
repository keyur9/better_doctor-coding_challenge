import os,sys
from helpers import *

source_data_file_name = 'source_data.json'
match_file_name = 'match_file.csv'

def main():
    # Read source_data_file
    parsed_json = get_json(source_data_file_name, multiple_jsons=True)

    # Store source data in a dict
    source_data = {}
    for data in parsed_json:
        npi = data['doctor']['npi']
        source_data[npi] = data

    # Read csv data into DataFrame
    match_df = get_dataframe_from_csv(match_file_name)

    matched_list = []
    non_match_list = []

    for index, row in match_df.iterrows():
        npi = row['npi']
        try:
            # Find practice data in source_data hash
            practice_data = find_by_npi(source_data, npi)

            # Match doctor name
            match_first_name(practice_data, row)
            match_last_name(practice_data, row)

            # Match address
            match_address(practice_data, row)

            matched_list.append(index)
        except Exception as e:
            non_match_list.append({index: e.message})

    print 'Final Result:'
    print 'Number of Matched fields: {}'.format(len(matched_list))
    print 'Number of Not Matched fields: {}'.format(len(non_match_list))


if __name__ == '__main__':
    main()
