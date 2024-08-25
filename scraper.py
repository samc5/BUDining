#beautiful soup and request imports
from bs4 import BeautifulSoup
import requests
import time
#url = 'https://www.bu.edu/dining/location/marciano/#menu'
import gc
def get_url(loc):
    return 'https://www.bu.edu/dining/location/' + loc + '/#menu'
def get_meals(url):
    # URL of the webpage

    # Send an HTTP GET request to the webpage
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
    # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')
        if soup.find('li', class_='js-meal-period-breakfast menu-meal-period') is None:
            breakfast = None
        else:
            breakfast = soup.find('li', class_='js-meal-period-breakfast menu-meal-period')
        if soup.find('li', class_='js-meal-period-lunch menu-meal-period') is None:
            lunch = None   
        else:
            lunch = soup.find('li', class_='js-meal-period-lunch menu-meal-period')
        if soup.find('li', class_='js-meal-period-dinner menu-meal-period') is None:
            dinner = None
        else:
            dinner = soup.find('li', class_='js-meal-period-dinner menu-meal-period')

        #find the menu items for each meal
        if breakfast is None:
            breakfast_items = None
        else:
            breakfast_items = breakfast.find_all('li', class_='menu-item')
        if lunch is None:
            lunch_items = None
        else:
            lunch_items = lunch.find_all('li', class_='menu-item')
        if dinner is None:
            dinner_items = None
        else:
            dinner_items = dinner.find_all('li', class_='menu-item')
        #set meals to all not-none items variables
        meals = []
        if breakfast_items is not None:
            meals.append(breakfast_items)
        if lunch_items is not None:
            meals.append(lunch_items)
        if dinner_items is not None:
            meals.append(dinner_items)
        return meals
    else:
        print(f"Failed to retrieve the webpage (Status Code: {response.status_code})")
        return None
    
def meals_test(url):
    """Fetches meals from the url, but uses the current date instead of not specifying date"""
    # URL of the webpage
    current_time = time.localtime()
    yr = current_time.tm_year
    mon = current_time.tm_mon
    day = current_time.tm_mday
    if mon < 10:
        mon = '0' + str(mon)
    if day < 10:
        day = '0' + str(day)
    yr_mon_day = str(yr) + '-' + str(mon) + '-' + str(day)
    # print(yr_mon_day)
    # Send an HTTP GET request to the webpage
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
    # Parse the HTML content of the page
        soup1 = BeautifulSoup(response.text, 'html.parser')
        response = None
        gc.collect()
        # print(soup1)

        # if soup1.find('ol', {'class': 'js-menu-bydate menu-area background-opaque menubydate-active', 'data-menudate': yr_mon_day}) is None:
        #     soup = soup1
        #     print("condition 1")
        # else:
        #print("condition 2")
        # clear = soup1.find('aside', class_='menu-warning')
        # print(f'clear: {clear}')
        # if clear is not None:
        #     return "No menu"
        soup = soup1.find('ol', {'data-menudate': yr_mon_day})
        soup1 = None
        gc.collect()
        #print(f'soup: {soup}')
        if soup.find('li', class_='js-meal-period-breakfast menu-meal-period') is None:
            breakfast = None
        else:
            breakfast = soup.find('li', class_='js-meal-period-breakfast menu-meal-period')
        if soup.find('li', class_='js-meal-period-lunch menu-meal-period') is None:
            lunch = None   
        else:
            lunch = soup.find('li', class_='js-meal-period-lunch menu-meal-period')
        if soup.find('li', class_='js-meal-period-dinner menu-meal-period') is None:
            dinner = None
        else:
            dinner = soup.find('li', class_='js-meal-period-dinner menu-meal-period')

        #find the menu items for each meal
        if breakfast is None:
            breakfast_items = None
        else:
            breakfast_items = breakfast.find_all('li', class_='menu-item')
        if lunch is None:
            lunch_items = None
        else:
            lunch_items = lunch.find_all('li', class_='menu-item')
        if dinner is None:
            dinner_items = None
        else:
            dinner_items = dinner.find_all('li', class_='menu-item')
        #set meals to all not-none items variables
        meals = []
        if breakfast_items is not None:
            meals.append(breakfast_items)
        if lunch_items is not None:
            meals.append(lunch_items)
        if dinner_items is not None:
            meals.append(dinner_items)
        return meals
    else:
        print(f"Failed to retrieve the webpage (Status Code: {response.status_code})")
        return None
    

def get_menu_items(meals):    #returns a list of lists of menu items with title, ingredients, and station
    ans = []
    titles = ""
    j = 0
    for meal in meals:
        for i in meal:
            bool = False
            j += 1
            if i.find('aside', class_='nutrition-facts-ingredients') is None:
                ingredients = 'none'
            else:
                ingredients = i.find('aside', class_='nutrition-facts-ingredients').get_text()
                titles += ingredients[-5:]
            if i.find('h4', class_='js-nutrition-open-alias menu-item-title') is None:
                title = 'none'
            else:
                title = i.find('h4', class_='js-nutrition-open-alias menu-item-title').get_text()
                if titles.find(ingredients[-5:] + title) != -1:
                    bool = True
                titles += title

            if i.find('strong', class_='js-sortby-station') is None:
                station = 'none'
            else:   
                station = i.find('strong', class_='js-sortby-station').get_text()
            meal_type = 'none'
            if len(meals) == 3:
                if meals[0] is not None and i in meals[0]:
                    meal_type = 'breakfast'
                elif meals[1] is not None and i in meals[1] and not bool:
                    #print(titles)
                    meal_type = 'lunch'
                elif meals[2] is not None and i in meals[2]:
                    meal_type = 'dinner'
                else:
                    meal_type = 'dinner'
            elif len(meals) == 2:
                if meals[0] is not None and i in meals[0]:
                    meal_type = 'lunch'
                elif meals[1] is not None and i in meals[1]:
                    meal_type = 'dinner'
                else:
                    meal_type = 'dinner'

            
            #print(title)
            #print(ingredients)
            ans.append([title, ingredients, station, meal_type, j])
           #print(ans[-1])
        #print(i.find('h4', class_='js-nutrition-open-alias menu-item-title').get_text())
    return ans

"""
---------------------------
Keywords for meat and gluten and random things
----------------------------
"""

meats_list = ['chicken', 'beef', 'pork', 'salmon', 'tuna', 'shrimp', 'fish', 'turkey', 'bacon', 'sausage', 'ham', 'meat', 'meatball', 'meatballs', 'meatloaf', 'crab', 'lobster']
gluten_list = ['wheat', 'barley', 'orzo', 'calise','malted', 'potato roll', 'focaccia', 'dough croissant pain', 'pita', 'assorted cookies', 'wonton skin', 'durum', 'create your own noodle salad', 'dnu - bread flat', 'roll kaiser 4']
sg_list = ['fresh basil', 'pomodoro sauce', 'marinara sauce', 'olive oil', 'grill works', 'maple glaze']
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

def contains_flag(menu_item, flag_lists): #returns true if an item contains a flag keyword
    for lst in flag_lists:
        for i in lst:
            if menu_item.find(i) != -1:
                return True
    return False


def contains_meat(menu_item): #returns true if an item contains a meat keyword
    for i in meats_list:
        if menu_item.find(i) != -1:
            return True
    return False

def contains_gluten(menu_item): #returns true if an item contains a gluten keyword
    for i in gluten_list:
        if menu_item.find(i) != -1:
            return True
    return False

def contains_egg(menu_item): #returns true if an item contains a egg keyword
    if menu_item.find('egg') != -1 or menu_item.find('omelet') != -1:
        return True
    else:
        return False



def is_sauce_or_garnish(menu_item): #returns true if an item is a sauce or garnish
    for i in sg_list:
        if menu_item.find(i) != -1:
            return True
    return False

def get_gf_menu(meals): # returns only foods that don't contain gluten keywords
    overall_menu = get_menu_items(meals)
    gf_menu = []
    for i in overall_menu:
        if contains_gluten(i[1].lower()) == False and contains_gluten(i[0].lower()) == False:
            gf_menu.append(i)
    return gf_menu


def get_gf_vegetarian_menu(meals):
    overall_menu = get_gf_menu(meals)
    gf_vegetarian_menu = []
    for i in overall_menu: #if it does not contain the words chicken, beef, pork, salmon, tuna, shrimp, fish, turkey, bacon, sausage, ham, meat, meatball, meatballs, meatloaf
        if contains_meat(i[1].lower()) == False and contains_meat(i[0].lower()) == False and contains_egg(i[0].lower()) == False and is_sauce_or_garnish(i[0].lower()) == False:
            gf_vegetarian_menu.append(i)
    return gf_vegetarian_menu
   



#print(get_menu_items(meals))
#print(get_gf_menu(meals))
#print(get_gf_vegetarian_menu(meals))

def sort_items_by_station(menu): #sort the results of a get_gf_vegetarian_menu call by station, into a dictionary
    ans = {}
    for i in menu:
        station = i[2].strip()
        if station in ans:
            ans[station].append(i)
        else:
            ans[station] = [i]
    return ans




def sort_important_items(sorted_menu): #clean the results of a sort_items_by_station call by removing all items from the salad bar, bakery, and deli, but leaving their station names as empty keys in the dictionary
    ans = {}
    for i in sorted_menu:
        if i != 'Salad Bar' and i != 'Bakery' and i != 'Deli' and i != 'Home Zone' and i != 'Fiesta' and i != 'Hot Breakfast Cereals':
            ans[i] = sorted_menu[i]
        else:
            ans[i] = []
    return ans
"""
This next function makes two dictionaries, the first one is the stations where the ingredients are necessary, and the second one is the stations where the titles are basically ingredients themselves
"""
def separate_important_items(sorted_menu): #return two dictionaries, one with the important items, and one with the unimportant items
    ans = {}
    ans2 = {}
    arr = []
    for i in sorted_menu:
        if i != 'Salad Bar' and i != 'Bakery' and i != 'Deli' and i != 'Home Zone' and i != 'Fiesta' and i != 'Hot Breakfast Cereals' and i != 'Paseo' and i != 'Grill Condiments and More' and i != 'none':
            ans[i] = sorted_menu[i]
        elif i != 'none':
            ans2[i] = sorted_menu[i]
    arr = [ans, ans2]
    return arr

def filter_separated_menu(separated_menu, filter_list): #filter the separated menu dict by a list of keywords
    ans = {}
    ans2 = {}
    arr = []
    ans3 = separated_menu[0]
    ans4 = separated_menu[1]
    
    for i in separated_menu[0]:
        for j in separated_menu[0][i]:
            #print(j[0],j[1], j[2], j[3])
            if contains_flag(j[0].lower(), filter_list) == False and contains_flag(j[1].lower(), filter_list) == False:
                if i in ans:
                    ans[i].append(j)
                else:
                    ans[i] = [j]
    for i in separated_menu[1]:
        for j in separated_menu[1][i]:
            if contains_flag(j[0].lower(), filter_list) == False and contains_flag(j[1].lower(), filter_list) == False:
                if i in ans2:
                    ans2[i].append(j)
                else:
                    ans2[i] = [j]
    arr = [ans, ans2]
    return arr

