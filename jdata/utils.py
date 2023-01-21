""" utils for working with json-format file"""

import json
from pprint import pprint


def load_from_json_file(filename: str = './flightplans.json') -> dict:
    """ load any information from json-format file and return it"""

    # if we need load from extermal site
    # response = urllib.request.urlopen(external_adr)
    # data = json.loads(response.read())

    # load from file
    with open(filename, 'r', encoding='utf-8') as fh:  # open file
        data = json.load(fh)  # load data

    fh.close()
    # at this point we can decipher data and put to my structure
    # but in first version we will return all data 'as is'
    return data


# this block for a self-test
if __name__ == '__main__':

    f_planes_data = load_from_json_file()
    if len(f_planes_data) != 0:
        print("FLIGHT_PLANS was opened and data were load")
        pprint(f_planes_data)
    else:
        print("we have some troubles with opening file 'FLIGHT_PLANS'")
