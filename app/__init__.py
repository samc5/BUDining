from flask import Flask, render_template
import main_tools as main
app = Flask(__name__)


url = 'https://www.bu.edu/dining/location/warren/#menu'

@app.route("/")       
def hello_world():
    return render_template('main.html')

@app.route("/menu")
def tester():

    arrays = main.separate_important_items(main.sort_items_by_station(main.get_gf_vegetarian_menu(main.get_meals(url))))

    return render_template('menu.html', arr = arrays)

@app.route("/menu/<loc>", methods = ["POST", "GET"])
def result(loc):
    url = 'https://www.bu.edu/dining/location/' + loc + '/#menu'
    arrays = main.separate_important_items(main.sort_items_by_station(main.get_gf_vegetarian_menu(main.get_meals(url))))
    return render_template('menu.html', arr = arrays)

if __name__ == "__main__":  # true if this file NOT imported
    app.debug = True        # enable auto-reload upon code change
    app.run()               # launch Flask