""" utils for working with json-format file"""

import json
# from pprint import pprint


def load_from_json_file(filename: str = './flightplans.json') -> dict:
    """ load any information from json-format file and return it"""

    # if we need load from external site
    # response = urllib.request.urlopen(external_adr)
    # data = json.loads(response.read())

    # load from file
    with open(filename, 'r', encoding='utf-8') as fh:  # open file
        data = json.load(fh)  # load data

    fh.close()
    # at this point we can decipher data and put to my structure
    # but in first version we will return all data 'as is'
    return data


def load_table_from_txt(filename: str = './table.txt') -> list[dict[str, str]]:
    tmp_list = []
    with open(filename, 'r') as fh:
        for readline in fh:
            if readline == '\n':
                break
            tmp_dict = {'icon': "",
                        'name': (readline.split('|'))[2],
                        'cat': readline.split('|')[3],
                        'kcal': readline.split('|')[4]}
            # print(readline.split('|'))
            tmp_list.append(tmp_dict)
    # print(tmp_list)
    filename_out = filename + '.json'
    with open(filename_out, 'w', encoding='utf-8') as fh:  # open file
        # data = json.load(fh)  # load data
        json.dump(tmp_list, fh)
    return tmp_list


# this block for a self-test
if __name__ == '__main__':

    # # test block
    # f_planes_data = load_from_json_file()
    # if len(f_planes_data) != 0:
    #     print("FLIGHT_PLANS was opened and data were load")
    #     pprint(f_planes_data)
    # else:
    #     print("we have some troubles with opening file 'FLIGHT_PLANS'")

    load_table_from_txt()
