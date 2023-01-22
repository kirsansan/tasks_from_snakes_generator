""" lesson1 part2 POST requests

    this code written by Kirill.S (Mr.K)
"""

from flask import Flask, render_template, request, url_for, abort, make_response
from alphabet.alphabet_def import alphabet
from utils.utils import prepare_menu
from config.config import OFFSET_ON_PAGE, FILE_FLIGHTPLANS
from config.table_of_content import site_menu, lesson1_menu
from jdata.utils import load_from_json_file
from flight.flight import Flight
from pprint import pprint
from people.people import People
from dataclasses import dataclass, asdict, astuple


app = Flask(__name__)

# GLOBAL VARIABLES
global_counter: int = 0
data = {"value": 1}
items = ["alpha", "bravo", "charlie"]
enrollments = [
    {"name": "alex", "phone": "+123456789"},
]
users = [
    {"pk": 1, "name": "alex", "phone": "+123456789"},
    {"pk": 2, "name": "mary", "phone": "+987654321"}
]
users_2 = [
    {"name": "alex", "phone": "+123456789"},
    {"name": "mary", "phone": "+987654321"}
]

@app.route('/test1', methods=['POST', 'GET'])
def post_counter():
    """Будем просто прибавлять к значению единичку при каждом запросе
    чтобы мы смогли это сделать видимо придется использовать некие глобальные переменные.
    Спросить у Автора
    """
    # if request.method == 'POST':
    #    pprint(request.form)
    # print(request.form)
    global data
    data['value'] += 1
    return str(data['value'])


@app.route('/test2', methods=['POST'])
def add_word():
    """ wait request as ('name': 'delta')
    в задаче сказано передать просто валью, но что postman что вообще идеалогия post-запросов
    всегда подразумевает кортеж ключ:значение  Надо спросить у Автора """
    # if request.method == 'POST':
    #    pprint(request.form)
    global items
    # print(request.args)

    items.append(request.form['name'])
    return items

@app.route('/test3', methods=['POST'])
def add_dict_record():
    """ wait request as ({"name": "mary", "phone": "+987654321"})
    """
    # if request.method == 'POST':
    print(request.form)
    global enrollments
    # *x, = enrollments[0].keys()    # очень странный оператор. save it for a history
    # print(x)
    # надо ли что-то тут еще проверять, например что в запросе верные ключи и они там есть??
    keys = list(enrollments[0].keys())    # take keys and will be sure in theirs names
    enrollments.append({keys[0]: request.form[keys[0]], keys[1]: request.form[keys[1]]})
    return enrollments

@app.route('/test4', methods=['POST'])
def get_new_dict_record_with_pk():
    """ wait request as ({"name": "mary", "phone": "+987654321"})
    but fill users dict with id: int = последний + 1
    """
    # if request.method == 'POST':
    # print(request.form)
    global users

    # if we want to work with dictionary
    max_user_pk = users[0]['pk']
    for user in users:  # we need to find maximum pk in users
        max_user_pk = max(max_user_pk, user['pk'])
    # return {"pk": max_user_pk + 1, "name": request.form['name'], "phone": request.form['phone']}

    # if we want to work with dataclass
    # person = People(pk=max_user_pk, name=request.form['name'], phone=request.form['phone'])
    person = People(request.form['name'], request.form['phone'], max_user_pk + 1)
    # print(astuple(person))
    return asdict(person)


@app.route('/test5', methods=['POST', 'GET'])
def add_dict_record_with_verify():
    """ add data from request to dict user_2 and return this dict
    wait request as ({"name": "mary", "phone": "+987654321"})
    however in case absense we need to return ["name missed", "phone missed"] and 400 code
    """
    # handle the GET request
    if request.method == 'GET':
        return '''
               <form method="POST">
                   <div><label>Name: <input type="text" name="name"></label></div>
                   <div><label>Phone: <input type="text" name="phone"></label></div>
                   <input type="submit" value="Submit">
               </form>'''
    # otherwise handle the POST request
    else:
        global users_2
        error_struct = []
        is_wrong_flag = False
        keys = list(users_2[0].keys())
        print(keys)
        for k in keys:
            if not request.form.get(k) or request.form.get(k) == "":
                error_struct.append(f"{k} missed")
                is_wrong_flag = True
        if is_wrong_flag:
            print(error_struct)
            return error_struct, 400
        else:
            users_2.append({keys[0]: request.form[keys[0]], keys[1]: request.form[keys[1]]})
            return users_2


@app.route('/test6', methods=['POST'])
def get_new_dict_records_requested_by_json():
    """ wait request in json format
    and....
    """
    # if request.method == 'POST':
    #     print(request.form)
    global users_2
    keys = list(users_2[0].keys())
    # is_wrong_flag_4_one = False
    is_wrong_flag_4_all = False

    request_data = request.get_json()
    for one_data_piece in request_data:
        # print(one_data_piece)
        is_wrong_flag_4_one = False
        for k in keys:
            if (k not in one_data_piece.keys()) or one_data_piece[k] == "":
                # error_struct.append(f"{k} missed") # если надо что-то рассказать при ответе на запрос
                is_wrong_flag_4_one = True
                is_wrong_flag_4_all = True
        if not is_wrong_flag_4_one:
            tmp_dict = {}
            for k in keys:
                tmp_dict[k] = one_data_piece[k]
            users_2.append(tmp_dict)
    """в примере вывода надо было отдать {"users_count": 4}, 
    но в условии самой задачи как-то неявно это пребуется отдать
    могу и так и эдак. спросить у Автора"""
    # if is_wrong_flag_4_all:
    #     return {'user_count': len(users_2)}, 400
    # else:
    #     return {'user_count': len(users_2)}
    if is_wrong_flag_4_all:
        return users_2, 400
    else:
        return users_2


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
