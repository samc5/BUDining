"""Main file for the API."""

import json

import sys
sys.path.append('\\data')
from flask import Blueprint, Response
#import firebase_db
#import scraper
import firebase_db
import scraper
#from data import firebase_db
#from data import scraper
#from api.data import data
#from api.data import firebase_db
import time
from datetime import datetime

# create a api blueprint
api_bp = Blueprint("API", __name__)

#data = data.Data()  # this is where all the data is stored
#stock = stock.Stock(data)
#news = news.News(data)

db = firebase_db.FirebaseDB()

# ==============================================================================

def update_data_gf_veg(forced):
    response = None
    if not forced:
        if check_metadata():
            return response
    # warren = scraper.separate_important_items(scraper.sort_items_by_station(scraper.get_gf_vegetarian_menu(scraper.get_meals(scraper.get_url("warren")))))
    # west = scraper.separate_important_items(scraper.sort_items_by_station(scraper.get_gf_vegetarian_menu(scraper.get_meals(scraper.get_url("west")))))
    # marciano = scraper.separate_important_items(scraper.sort_items_by_station(scraper.get_gf_vegetarian_menu(scraper.get_meals(scraper.get_url("marciano")))))
    # granby = scraper.separate_important_items(scraper.sort_items_by_station(scraper.get_gf_vegetarian_menu(scraper.get_meals(scraper.get_url("granby")))))
    warren = scraper.separate_important_items(scraper.sort_items_by_station(scraper.get_gf_vegetarian_menu(scraper.meals_test(scraper.get_url("warren")))))
    west = scraper.separate_important_items(scraper.sort_items_by_station(scraper.get_gf_vegetarian_menu(scraper.meals_test(scraper.get_url("west")))))
    marciano = scraper.separate_important_items(scraper.sort_items_by_station(scraper.get_gf_vegetarian_menu(scraper.meals_test(scraper.get_url("marciano")))))
    granby = scraper.separate_important_items(scraper.sort_items_by_station(scraper.get_gf_vegetarian_menu(scraper.meals_test(scraper.get_url("granby")))))
    lt = time.localtime()
    meta = {"last_updated": {"tm_year": lt.tm_year, "tm_mon": lt.tm_mon, "tm_mday": lt.tm_mday, "tm_hour": lt.tm_hour, "tm_min": lt.tm_min, "tm_sec": lt.tm_sec, "tm_yday": lt.tm_yday}}
    response = {"warren": warren, "west": west, "marciano": marciano, "granby": granby, "meta": meta}
    print("down to update data")
    db.update_db_data(response)
    return response

def update_data(forced):
    response = None
    if not forced:
        if check_metadata():
            return response
    # warren = scraper.separate_important_items(scraper.sort_items_by_station(scraper.get_gf_vegetarian_menu(scraper.get_meals(scraper.get_url("warren")))))
    # west = scraper.separate_important_items(scraper.sort_items_by_station(scraper.get_gf_vegetarian_menu(scraper.get_meals(scraper.get_url("west")))))
    # marciano = scraper.separate_important_items(scraper.sort_items_by_station(scraper.get_gf_vegetarian_menu(scraper.get_meals(scraper.get_url("marciano")))))
    # granby = scraper.separate_important_items(scraper.sort_items_by_station(scraper.get_gf_vegetarian_menu(scraper.get_meals(scraper.get_url("granby")))))4
    warren = scraper.separate_important_items(scraper.sort_items_by_station(scraper.get_menu_items(scraper.meals_test(scraper.get_url("warren")))))
    west = scraper.separate_important_items(scraper.sort_items_by_station(scraper.get_menu_items(scraper.meals_test(scraper.get_url("west")))))
    marciano = scraper.separate_important_items(scraper.sort_items_by_station(scraper.get_menu_items(scraper.meals_test(scraper.get_url("marciano")))))
    granby = scraper.separate_important_items(scraper.sort_items_by_station(scraper.get_menu_items(scraper.meals_test(scraper.get_url("granby")))))
    lt = time.localtime()
    meta = {"last_updated": {"tm_year": lt.tm_year, "tm_mon": lt.tm_mon, "tm_mday": lt.tm_mday, "tm_hour": lt.tm_hour, "tm_min": lt.tm_min, "tm_sec": lt.tm_sec, "tm_yday": lt.tm_yday}}
    response = {"warren": warren, "west": west, "marciano": marciano, "granby": granby, "meta": meta}
    print("down to update data")
    db.update_db_data(response)
    return response



# ==============================================================================
def check_metadata():
    """Returns true if the metadata tm_year and tm_yday is the same as the current year and day"""
    meta = db.get_db_meta()
    lt = time.localtime()
    if meta["last_updated"]["tm_year"] == lt.tm_year and meta["last_updated"]["tm_yday"] == lt.tm_yday:
        return True
    else:
        return False

#update_data(True)

def update_stock_data(request_time):
    """Update the stock data."""
    response = None
    if not stock.load_stock_data(db):
        stock.save_closings_prices()
        stock.save_current_prices()

        # separate db update from the rest of the code
        # this is so that the stock data will only update when necessary
        response = stock.get_stock_data(request_time)
        db.update_stock_data(response)
    else:
        response = stock.get_stock_data(request_time)

    return response

def get_warren_dict():
    """Get the daily menu from Warren from the Firebase database."""
    return db.get_warren()
def get_west_dict():
    """Get the daily menu from West from the Firebase database."""
    return db.get_west()
def get_marciano_dict():
    """Get the daily menu from Marciano from the Firebase database."""
    return db.get_marciano()
def get_granby_dict():
    """Get the daily menu from Granby from the Firebase database."""
    return db.get_granby()
def get_meta_dict():
    """Get the metadata from the Firebase database."""
    return db.get_db_meta()

