"""Flask for the web design of the website."""
from flask import Flask, render_template
"""os for the os.path.join function."""
from flask import request
from flask import redirect
import os
import sys
sys.path.append('\\api')
sys.path.append('\\api\\data')
from api import api
from api.data import scraper
#sys.path = [curr_path]
app = Flask(__name__)


BASE_URL = 'https://www.bu.edu/dining/location/warren/#menu'

"""
---------------------------
Keywords for meat and gluten and random things
----------------------------
"""

meats_list = ['chicken', 'beef', 'pork', 'salmon', 'tuna', 'shrimp', 'fish', 'turkey', 'bacon', 'sausage', 'ham', 'meat', 'meatball', 'meatballs', 'meatloaf', 'crab', 'lobster']
gluten_list = ['wheat', 'barley', 'orzo', 'calise','malted', 'potato roll', 'focaccia', 'dough croissant pain', 'pita', 'assorted cookies', 'durum', 'create your own noodle salad', 'dnu - bread flat', 'roll kaiser 4']
sg_list = ['fresh basil', 'pomodoro sauce', 'marinara sauce', 'olive oil', 'grill works']
dairy_list = ['yogurt', 'milk', 'cheese', 'ice cream', 'butter']
peanut_list= ['peanut', 'peanuts', 'peanut butter', 'peanutbutter']
soy_list = ['soy', 'soybean', 'soybeans', 'soy sauce', 'tofu']
egg_list = ['egg', 'eggs', 'omelet', 'omelets']
tree_nut_list = ['cashew', 'pecan', 'walnut', 'almond', 'pistachio','brazil nut', 'hazelnut', 'macadamia nut', 'pine nut']
shellfish_list = ['crab', 'lobster', 'shrimp', 'prawn', 'crawfish', 'crayfish', 'mussel', 'oyster', 'clam', 'squid', 'scallop', 'snail', 'escargot']
pesc_meats_list = ['chicken', 'beef', 'pork', 'turkey', 'bacon', 'sausage', 'ham', 'meat', 'meatball', 'meatballs', 'meatloaf']
wheat_list = ['wheat', 'orzo', 'calise','malted', 'durum', 'dnu - bread flat', 'roll kaiser 4', 'potato roll', 'pita', 'semolina', 'dough croissant pain', 'focaccia', 'create your own noodle', 'assorted cookies']
sesame_list = ['sesame', 'sesame seed', 'sesame seeds', 'sesame oil', 'sesame paste', 'tahini']
mustard_list = ['mustard']
vegan_list = meats_list + dairy_list + egg_list

allergen_map = {'Gluten Free': gluten_list, 'Dairy Free': dairy_list, 'Vegetarian': meats_list, 'Vegan': vegan_list, 'Pescatarian': pesc_meats_list, 'Peanut': peanut_list, 'Tree Nut': tree_nut_list, 'Soy': soy_list, 'Egg': egg_list, 'Shellfish': shellfish_list, 'Wheat': wheat_list, 'Sesame': sesame_list, 'Mustard': mustard_list}

dining_hall_list = ['Warren', 'West', 'Marciano']

@app.route("/")       
def hello_world():
    """Redirect to home page."""
    return redirect("/home")

@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/menu", methods = ["POST", "GET"])
def tester():
    """runs /menu, which is obsolete/unecessary, mostly so it doesn't crash"""
    if request.form:
        selected_interests = request.form.getlist('interests')
        list_restrictions = []
        for interest in selected_interests:
            list_restrictions.append(allergen_map[interest])
        #print(list_restrictions)
        api.update_data(False)
        arrays0 = {"Warren": api.get_warren_dict(), "West": api.get_west_dict(), "Marciano": api.get_marciano_dict()}
        arrays1 = []
        arrays = api.get_warren_dict()
        arrays2 = scraper.filter_separated_menu(arrays, list_restrictions)
        for i in range(len(dining_hall_list)):
             print(i)
             #print(arrays0[i])
             arrays1.append(scraper.filter_separated_menu(arrays0[dining_hall_list[i]], list_restrictions))
             #arrays[i].append(dining_hall_list[i])
             print(f'{i} worked')
             # add dining hall name to the array
             #arrays[i].append(dining_hall_list[i])
        return render_template('menu.html', arrs = arrays1, names=dining_hall_list, lenn = range(len(dining_hall_list)))
    #arrays = main.separate_important_items(main.sort_items_by_station(main.get_gf_vegetarian_menu(main.get_meals(BASE_URL))))

    return render_template('main.html')

# @app.route("/menu/<loc>", methods = ["POST", "GET"])
# def result(loc):
#     """The main sever function for now, runs the website based on the location of dining hall"""
#     url = 'https://www.bu.edu/dining/location/' + loc + '/#menu'
#     #file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'api/api.py')
#     #update data if needed
#     api.update_data(False)
#     if loc == "warren":
#         arrays = api.get_warren_dict()
#     elif loc == "west":
#         arrays = api.get_west_dict()
#     elif loc == "marciano":
#         arrays = api.get_marciano_dict()
#     else:
#         arrays = api.get_granby_dict()
#     #arrays = main.separate_important_items(main.sort_items_by_station(main.get_gf_vegetarian_menu(main.get_meals(url))))
#     print(arrays)
#     return render_template('menu.html', arr = arrays)

if __name__ == "__main__":  # true if this file NOT imported
    app.debug = True        # enable auto-reload upon code change
    app.run()               # launch Flask