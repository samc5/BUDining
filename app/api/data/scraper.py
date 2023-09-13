#beautiful soup and request imports
from bs4 import BeautifulSoup
import requests

#url = 'https://www.bu.edu/dining/location/marciano/#menu'

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

def get_menu_items(meals):    #returns a list of lists of menu items with title, ingredients, and station
    ans = []
    for meal in meals:
        for i in meal:
            if i.find('h4', class_='js-nutrition-open-alias menu-item-title') is None:
                title = 'none'
            else:
                title = i.find('h4', class_='js-nutrition-open-alias menu-item-title').get_text()
            if i.find('aside', class_='nutrition-facts-ingredients') is None:
                ingredients = 'none'
            else:
                ingredients = i.find('aside', class_='nutrition-facts-ingredients').get_text()
            if i.find('strong', class_='js-sortby-station') is None:
                station = 'none'
            else:   
                station = i.find('strong', class_='js-sortby-station').get_text()
            
            #print(title)
            #print(ingredients)
            ans.append([title, ingredients, station])
        #print(i.find('h4', class_='js-nutrition-open-alias menu-item-title').get_text())
    return ans

"""
---------------------------
Keywords for meat and gluten and random things
----------------------------
"""

meats_list = ['chicken', 'beef', 'pork', 'salmon', 'tuna', 'shrimp', 'fish', 'turkey', 'bacon', 'sausage', 'ham', 'meat', 'meatball', 'meatballs', 'meatloaf', 'crab', 'lobster']
gluten_list = ['wheat', 'barley', 'orzo', 'calise', 'malt', 'potato roll', 'focaccia', 'dough croissant pain', 'pita', 'assorted cookies', 'durum', 'create your own noodle salad']
sg_list = ['fresh basil', 'pomodoro sauce', 'marinara sauce', 'olive oil', 'grill works']
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
        if i[2] in ans:
            ans[i[2]].append(i)
        else:
            ans[i[2]] = [i]
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
        if i != 'Salad Bar' and i != 'Bakery' and i != 'Deli' and i != 'Home Zone' and i != 'Fiesta' and i != 'Hot Breakfast Cereals' and i != 'none':
            ans[i] = sorted_menu[i]
        elif i != 'none':
            ans2[i] = sorted_menu[i]
    arr = [ans, ans2]
    return arr






# #print statements for sort_important_items, print a "-------------------------" before and after station name
# for i in sort_items_by_station(get_gf_vegetarian_menu(meals)):
#     print("-------------------------")
#     print(i)
#     print("-------------------------")
#     for j in sort_important_items(sort_items_by_station(get_gf_vegetarian_menu(meals)))[i]:
#         print(j[0])

#print statements for separate_important_items, print a "-------------------------" before and after station name


# print(separate_important_items(sort_items_by_station(get_gf_vegetarian_menu(get_meals(url))))[0])
# print("-------------------------")
# print(separate_important_items(sort_items_by_station(get_gf_vegetarian_menu(get_meals(url))))[1])

# for i1 in separate_important_items(sort_items_by_station(get_gf_vegetarian_menu(get_meals(url))))[1]:
#     print("-------------------------")
#     print(i1)
#     print("-------------------------")
#     for j1 in separate_important_items(sort_items_by_station(get_gf_vegetarian_menu(get_meals(url))))[1][i1]:
#         print(j1[0])
