""" my project for learning python with flask
    this is a simple project for solve tasks from task book
    which was written by Gleb Kushedow (aka @kushedow aka t.me/kushedow)

    this code written by Kirill.S (Mr.K)
"""


from flask import Flask, render_template, request, url_for
from alphabet.alphabet_def import alphabet
from utils.utils import prepare_menu

app = Flask(__name__)

site_menu: list = []
#prepare_menu(site_menu)
site_menu = [{"name": "Lesson 1", "url": "/lesson1"},
             {"name": "Lesson 2", "url": "/lesson2"},
             {"name": "Lesson 3", "url": "/lesson3"},
             {"name": "Lesson 4", "url": "/lesson4"},
             {"name": "Lesson 5", "url": "/lesson5"}]
lesson1_menu = [{"name": "Hello", "url": "/user/Gleb"},
                {"name": "Task 1 letter", "url": "/letter/y"},
                {"name": "Task 2 find", "url": "/find/?letter=Q"},
                {"name": "Task 3 check", "url": "/check/B/Bravo"},
                {"name": "Task 4 between ", "url": "/between/?from=<letter>&to=<letter>"}]

@app.route('/')
def index():
    return render_template('index.html', title="ONE", menu=site_menu, submenu=lesson1_menu)

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
    return render_template('index.html', menu=site_menu, adout='<h1>Hello World! Do you want to have some test? </h1>')
    # return '<h1>Hello World! Do you want to have some test? </h1>'

@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, %s!</h1>' % name

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

    return

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
