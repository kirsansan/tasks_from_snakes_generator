""" my project for learning python with flask
    this is a simple project for solve tasks from task book
    which was written by Gleb Kushedow (aka @kushedow aka t.me/kushedow)

    this code written by Kirill.S (Mr.K)
"""
import flask
from flask import Flask, render_template, request, url_for, abort
from alphabet.alphabet_def import alphabet
from utils.utils import prepare_menu
from config.config import OFFSET_ON_PAGE, FILE_FLIGHTPLANS
from config.table_of_content import site_menu, lesson1_menu
from jdata.utils import load_from_json_file
from flight.flight import Flight
from pprint import pprint


app = Flask(__name__)

# GLOBAL VARIABLES
global_counter: int = 0

def create_list_of_flights() -> list[Flight]:
    data_ = load_from_json_file(FILE_FLIGHTPLANS)
    flights_list: list[Flight:] = []
    # pprint(data_)
    for one_item_flight_ in data_:
        tmp_fpl_ = Flight(**one_item_flight_)
        # print(tmp_fpl_)
        flights_list.append(tmp_fpl_)
    return flights_list


@app.route('/')
def index():
    return render_template('index.html', title="Задачник", menu=site_menu, submenu=lesson1_menu)

# def hello_world():  # put application's code here
#     word = request.args.get('num')
#     num_out = '123'
#     return render_template(
#         'tttt1.html',
#         word=word,
#         num_out=num_out
#     )


@app.route('/about')
def about():
    return render_template('about.html', menu=site_menu)


@app.route('/lesson1')
def lesson1():
    return render_template('lesson1.html', menu=site_menu, submenu=lesson1_menu)


@app.route('/test')
def hello_one_more_time():
    return render_template('hello.html',
                           title="test page",
                           menu=site_menu,
                           hello='Hello World! Do you want to have some test?')
    # return '<h1>Hello World! Do you want to have some test? </h1>'


@app.route('/user/<name>')
def user(name):
    # return '<h1>Hello, %s!</h1>' % name
    return render_template('hello.html', title="WOW", menu=site_menu, hello=f'Hello, {name}!')


@app.route('/letter/<letter>')
def name_from_letter(letter):
    str_letter = str(letter).upper()
    if str_letter in alphabet:
        return alphabet[str_letter]
    return "I dont know this character"


@app.route('/find/')
def name_from_letter_query():
    # letter = request.args.get('letter')
    str_letter = str(request.args.get('letter')).upper()
    if str_letter in alphabet:
        return alphabet[str_letter]
    return "I dont know this character"


@app.route('/check/<letter>/<word>')
def is_char_associate_word(letter, word):
    str_letter = str(letter).upper()
    # print(str_letter, str(word), alphabet[str_letter])
    if (str_letter in alphabet) and alphabet[str_letter] == str(word):
        return "True"
    return "False"


@app.route('/between/')
def find_between():
    """Handler for  'between/?from=<letter>&to=<letter>'
    """
    char_from = str(request.args.get('from')).upper()
    char_to = str(request.args.get('to')).upper()
    temp_str_for_answer = ""
    # print(alphabet.keys())
    # print(char_from, char_to)
    if char_to not in alphabet or char_from not in alphabet or char_from >= char_to:
        return "-"
    for x in alphabet:
        if (char_from < x) and (char_to > x):
            temp_str_for_answer += x
    if temp_str_for_answer == "":
        temp_str_for_answer = "-"
    return temp_str_for_answer


@app.route('/get-some/<number_as_str>')
def get_some_numbers(number_as_str: str):
    """Handler for /get-some/<number> """
    tmp_str_4_answer = ""
    counter = 0
    # if int(number_as_str) < len(alphabet):
    #    for index in range(0,int(number_as_str)):
    for x in alphabet:
        counter += 1
        if counter > int(number_as_str):
            break
        tmp_str_4_answer += x
    # tmp_str_4_answer = ["".join(x) for x in alphabet.keys()]
    if tmp_str_4_answer == "":
        tmp_str_4_answer = "-"
    return tmp_str_4_answer


@app.route('/letters/')
def get_some_slice():
    """"Handler for / letters /?limit = < limit > & offset = < offset >
    I need tell to Author about mistake with lower letters in his task-manual
    """
    limit = len(alphabet)
    if request.args.get('limit') and int(request.args.get('limit')) < 26:
        limit = int(request.args.get('limit'))
    offset = 0
    if request.args.get('offset') and int(request.args.get('offset')) > 0:
        offset = int(request.args.get('offset'))
    sort_direct = 1
    if request.args.get('sort') == 'desc':
        sort_direct = -1
    # print(limit, offset,  sort_direct)
    tmp_str_4_answer = ""
    alphabet_list = list(alphabet)
    if offset >= len(alphabet_list):
        return "-"
    if offset + limit >= len(alphabet_list):
        limit = len(alphabet_list) - offset
    if sort_direct < 0:
        offset = len(alphabet) - 1 - offset
    # print(limit, offset, sort_direct, offset + (limit * sort_direct))
    for i in range(offset, offset + (limit * sort_direct), sort_direct):
        tmp_str_4_answer += alphabet_list[i]
    return tmp_str_4_answer.lower()


@app.route('/letters/page/<page_number_as_str>')
def get_some_page(page_number_as_str):
    """Handler for /letters/page/<page_number>
    return string with 5 elements
    :param page_number_as_str: number for start-page from 0
    """
    offset_on_page = OFFSET_ON_PAGE
    page_number = int(page_number_as_str)
    alphabet_list = list(alphabet)
    if page_number * offset_on_page > len(alphabet_list):
        abort(404)
    if (page_number + 1) * offset_on_page > len(alphabet_list):
        return "".join(alphabet_list[page_number * offset_on_page: len(alphabet_list)])
    return "".join(alphabet_list[page_number * offset_on_page: (page_number + 1) * offset_on_page])


@app.route('/search/')
def search_substring_in_values():
    """Handler for /search/?s=<s> 
    take 's' substring as param for searching
    :return: all words that include substring or 404 error if not found
    """
    substring = request.args.get('s')
    tmp_str_4_answer = ""
    for x in alphabet:
        if substring.lower() in alphabet[x].lower():
            tmp_str_4_answer += " " + alphabet[x]
    if tmp_str_4_answer == "":
        abort(404)
    return tmp_str_4_answer


@app.route('/get/')
def search_substring_for_length():
    """Handler for /get/?len=<length>
    take 'len' as param for searching strings with length = len
    :return: all words that length == len or 404 error if not found
    """
    length = int(request.args.get('len'))
    tmp_str_4_answer = ""
    for x in alphabet:
        if len(alphabet[x]) == length:
            tmp_str_4_answer += " " + alphabet[x]
    if tmp_str_4_answer == "":
        abort(404)
    return tmp_str_4_answer


@app.route('/flights/')
def search_filghts_from_to():
    """flights/?from=<airport_1>&to=<airport_2>"""
    airport1 = request.args.get('airport_1')
    airport2 = request.args.get('airport_2')
    flights_list = create_list_of_flights()
    # data_ = load_from_json_file(FILE_FLIGHTPLANS)
    # # pprint(data_)
    # for one_item_flight_ in data_:
    #     tmp_fpl_ = Flight(**one_item_flight_)
    #     # print(tmp_fpl_)
    #     flights_list.append(tmp_fpl_)
    # print(flights_list)
    # print(airport1, airport2)
    prepare_answer_list = []
    [prepare_answer_list.append(x) for x in flights_list if x.from_ == airport1 and x.to == airport2]
    # print(prepare_answer_list)
    str_4_out = f"{airport1} > {airport2} /" \
                + "/".join([(x.number + " " + x.departure_time + " " + x.arriving_time)
                              for x in prepare_answer_list])
    if len(prepare_answer_list) == 0:
        str_4_out += "<p> Не найдено"
    # print(str_4_out)
    # return str_4_out
    return render_template('answer.html', menu=site_menu, mytext=str_4_out.split('/'))


@app.route('/flights/between/<airport_1>&<airport_2>')
def search_flights_between(airport_1, airport_2):
    """/flights/between/<airport_1>&<airport_2>"""
    flights_list = create_list_of_flights()
    prepare_answer_list = []
    [prepare_answer_list.append(x) for x in flights_list
        if (x.from_ == airport_1 and x.to == airport_2) or
            (x.from_ == airport_2 and x.to == airport_1)]
    str_4_out = f"{airport_1} < > {airport_2} /" \
                + "/".join([(x.number + " " + x.departure_time + " " + x.arriving_time)
                              for x in prepare_answer_list])
    # str_4_out = map(str, prepare_answer_list)
    if len(prepare_answer_list) == 0:
        str_4_out += "<p> Не найдено"
    # print(str_4_out)
    # return str_4_out
    return render_template('answer.html', menu=site_menu, mytext=str_4_out.split('/'))


@app.route('/flights/from/<airport1>/to/<airport2>')
def search_flights_from_to(airport1: str, airport2: str):
    """flights/from/<airport1>/to/<airport2>"""
    if (not airport1.isupper()) or (not airport2.isupper()):
        loc = f'/flights/from/{airport1.upper()}/to/{airport2.upper()}'
        return flask.redirect(location=loc, code=301)
    flights_list = create_list_of_flights()
    prepare_answer_list = []
    [prepare_answer_list.append(x) for x in flights_list if x.from_ == airport1 and x.to == airport2]
    # print(prepare_answer_list)
    str_4_out = f"{airport1} > {airport2} /" \
                + "/".join([(x.number + " " + x.departure_time + " " + x.arriving_time)
                              for x in prepare_answer_list])
    if len(prepare_answer_list) == 0:
        str_4_out += "<p> Не найдено"
    # print(str_4_out)
    # return str_4_out
    return render_template('answer.html', menu=site_menu, mytext=str_4_out.split('/'))

@app.route('/flights/from/<airport1>')
def flight_search_from(airport1: str):
    """Handler for /flights/from/<airport_1>
    кажется в  задании чего-то недоставало, нет списка военных аэропортов,
    и идет какая-то ссылка на название для вывода... подсказать автору
    """
    # flights_list = create_list_of_flights()
    military_airports = ['CKL', 'ZIA']
    if not airport1.isupper():
        return flask.redirect(location=f'/flights/from/{airport1.upper()}', code=308)
    if airport1 in military_airports:
        abort(403)
    # тут можно приделать серчилку по базе. но неясно надо ли, пока опустим
    # return "Аэропорт {0}".format(airport1)
    return render_template('answer.html', menu=site_menu, mytext=["Аэропорт {0}".format(airport1)])

@app.route('/flights/with=<plane_1>')
def search_for_planes(plane_1: str):
    """/flights/with=<plane_1>,<plane_2>
    в задании упомянуты СПИСКИ <plane_1>,<plane_2> ... неясно это неограниченный список или как
    окей - загнал как список и его сверяю
    """
    plane_1 = plane_1.split(",")
    flights_list = create_list_of_flights()
    prepare_answer_list = []
    [prepare_answer_list.append(x) for x in flights_list if x.plane in plane_1]
    print(plane_1, prepare_answer_list)
    str_4_out = " " + "/".join([(x.number + " " + x.from_ + " " + x.departure_time + " > "
                                    + x.arriving_time + " " + x.to) for x in prepare_answer_list]) + " "
    if len(prepare_answer_list) == 0:
        str_4_out += "<p> Не найдено"
    # print(str_4_out)
    # return str_4_out
    return render_template('answer.html', menu=site_menu, mytext=str_4_out.split('/'))

@app.route('/flights/nowith=<plane_3>')
def search_for_no_planes(plane_3: str):
    plane_1 = plane_3.split(",")
    flights_list = create_list_of_flights()
    prepare_answer_list = []
    [prepare_answer_list.append(x) for x in flights_list if x.plane not in plane_1]
    str_4_out = " " + "/".join([(x.number + " " + x.from_ + " " + x.departure_time + " > "
                                   + x.arriving_time + " " + x.to) for x in prepare_answer_list]) + " "
    if len(prepare_answer_list) == 0:
        str_4_out += "<p>Не найдено"
    # return str_4_out
    return render_template('answer.html', menu=site_menu, mytext=str_4_out.split('/'))


@app.route('/testPOS', methods=['POST', 'GET'])
def test_for_post():
    if request.method == 'POST':
        pprint(request.form)
    print(request.form)
    return render_template('answer.html', menu=site_menu, mytext=['test POS method'])

@app.route('/poscounter', methods=['POST'])
def post_counter():
    if request.method == 'POST':
        pprint(request.form)

    global global_counter
    global_counter += 1
    return render_template('hello.html', menu=site_menu, hello=[f'magic variable = {global_counter}'])


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
