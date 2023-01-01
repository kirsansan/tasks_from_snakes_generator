from flask import Flask, render_template, request

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

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
