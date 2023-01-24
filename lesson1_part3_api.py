""" lesson1 part3 get in API"""

from flask import Flask, request, abort
import random

app = Flask(__name__)

# global variables
shopping_list = ["milk", "sugar", "cookies", "corn-flakes", "nutella"]
ext_shopping_list = {
  "milk": 150,
  "sugar": 90,
  "cookies": 200,
  "corn-flakes": 140,
  "nutella": 270,
}
expenses_list = [
  {"name": "milk", "unit_price": 50, "amount": 3, "total": 150, "cat": "mil"},
  {"name": "sugar", "unit_price": 30, "amount": 3, "total": 90 },
  {"name": "cookies", "unit_price": 50, "amount": 4, "total": 200 },
  {"name": "corn-flakes", "unit_price": 70, "amount": 2, "total": 140 },
  {"name": "nutella", "unit_price": 125, "amount": 1, "total": 250 },
]

# @app.route('/api/1/random')
# def get_random():
#     return {"number": random.randint(0, 10)}

@app.route('/api/1/random')
def get_random_from_interval():
    """ /api/1/random?from=…&to=…

    :return: json based interval"""
    interval_start = 0
    interval_end = 10
    if request.args.get('from').isdigit() and request.args.get('to').isdigit():
        interval_start = int(request.args.get('from'))
    # if request.args.get('to').isdigit():
        interval_end = int(request.args.get('to'))
    # interval_end = int(request.args.get('to'))
    print("2")
    return {"number": random.randint(interval_start, interval_end)}


@app.route('/api/1/grocery')
def get_grocery():
    global shopping_list
    return shopping_list


@app.route('/api/1/grocery-stats')
def get_grocery_statistic():
    global ext_shopping_list
    prepare_answer = {"count": len(ext_shopping_list),
                      "total": sum(ext_shopping_list.values()),
                      "max": max(ext_shopping_list.values()),
                      "min": min(ext_shopping_list.values()),
                      "avg": round(sum(ext_shopping_list.values())/len(ext_shopping_list))}
    return prepare_answer

@app.route('/api/1/expanses/<product>')
def get_expenses(product):
    """GET /api/1/expanses/<product>"""
    global expenses_list
    for challenger in expenses_list:
        if challenger['name'] == product:
            return challenger
    abort(404)




if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
