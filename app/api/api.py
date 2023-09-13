"""Main file for the API."""

import json

from flask import Blueprint, Response
from data import firebase_db
from data import scraper
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

def update_data(forced):
    response = None
    if not forced:
        if check_metadata():
            return response
    else:
        warren = scraper.separate_important_items(scraper.sort_items_by_station(scraper.get_gf_vegetarian_menu(scraper.get_meals(scraper.get_url("warren")))))
        west = scraper.separate_important_items(scraper.sort_items_by_station(scraper.get_gf_vegetarian_menu(scraper.get_meals(scraper.get_url("west")))))
        marciano = scraper.separate_important_items(scraper.sort_items_by_station(scraper.get_gf_vegetarian_menu(scraper.get_meals(scraper.get_url("marciano")))))
        granby = scraper.separate_important_items(scraper.sort_items_by_station(scraper.get_gf_vegetarian_menu(scraper.get_meals(scraper.get_url("granby")))))
        lt = time.localtime()
        meta = {"last_updated": {"tm_year": lt.tm_year, "tm_mon": lt.tm_mon, "tm_mday": lt.tm_mday, "tm_hour": lt.tm_hour, "tm_min": lt.tm_min, "tm_sec": lt.tm_sec, "tm_yday": lt.tm_yday}}
        response = {"warren": warren, "west": west, "marciano": marciano, "granby": granby, "meta": meta}
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

update_data(True)

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


def update_news_data():
    """Update the news data."""
    if not news.load_news_data(db):
        with lock:
            # only one thread can update the news data at a time.
            # this saves API calls
            news.save_news(db)  # save the news data to the database

# ==============================================================================


@api_bp.route("/stock_data", methods=["GET"])
def get_stock():
    """Return company info, ticker, previous closing prices, and current prices."""

    request_time = str(datetime.now())
    response = update_stock_data(request_time)

    return Response(json.dumps(response), mimetype="application/json")


@api_bp.route("/news_data", methods=["GET"])
def get_news():
    """Return the news data."""

    request_time = str(datetime.now())
    update_news_data()

    response = news.get_news_data(request_time)

    return Response(json.dumps(response), mimetype="application/json")