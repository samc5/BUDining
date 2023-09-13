"""Flask for the web design of the website."""
from flask import Flask, render_template
"""main_tools for the main functions of the website."""
import main_tools as main
app = Flask(__name__)


BASE_URL = 'https://www.bu.edu/dining/location/warren/#menu'

@app.route("/")       
def hello_world():
    """Return base page. Mostly so it doesn't crash"""
    return render_template('main.html')

@app.route("/menu")
def tester():
    """runs /menu, which is incomplete, mostly so it doesn't crash"""

    arrays = main.separate_important_items(main.sort_items_by_station(main.get_gf_vegetarian_menu(main.get_meals(BASE_URL))))

    return render_template('menu.html', arr = arrays)

@app.route("/menu/<loc>", methods = ["POST", "GET"])
def result(loc):
    """The main sever function for now, runs the website based on the location of dining hall"""
    url = 'https://www.bu.edu/dining/location/' + loc + '/#menu'
    arrays = main.separate_important_items(main.sort_items_by_station(main.get_gf_vegetarian_menu(main.get_meals(url))))
    return render_template('menu.html', arr = arrays)

if __name__ == "__main__":  # true if this file NOT imported
    app.debug = True        # enable auto-reload upon code change
    app.run()               # launch Flask