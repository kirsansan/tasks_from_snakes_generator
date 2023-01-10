""" my project for learning python with flask
    this is a simple project for solve tasks from task book
    which was written by Gleb Kushedow (aka @kushedow aka t.me/kushedow)

    this code written by Kirill.S (Mr.K)
"""


from flask import Flask, render_template, request, url_for
from alphabet.alphabet_def import alphabet

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    word = request.args.get('num')
    num_out = '123'
    return render_template(
        'tttt1.html',
        word=word,
        num_out=num_out
    )

@app.route('/test')
def hello_one_more_time():
    return '<h1>Hello World! Do you want to have some test? </h1>'

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

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
