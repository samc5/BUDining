"""This file connects to the Firebase database and saves the data to Firebase realtime database."""

import os
import threading
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db



class FirebaseDB:
    """The class for connecting to and accessing the Firebase database."""

    def __init__(self):
        """Initialize the FirebaseDB class."""
        print(os.path.exists("serviceAccountKey.json"))
        #print(os.path.abspath("serviceAccountKey.json"))
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'serviceAccountKey.json')
        print(file_path)
        # check if serviceAccountKey.json exists using the absolute path
        if "serviceAccountKey.json" not in file_path:
            # throw an error
            raise FileNotFoundError(
                """The serviceAccountKey.json file does not exist.\n
            Create the serviceAccountKey.json file:\n
            1. Go to the Firebase console\n
            2. Click on the project\n
            3. Click on the gear icon and select Project Settings\n
            4. Click on the Service Accounts tab\n
            5. Click on the Generate new private key button\n
            6. Rename the downloaded JSON file to serviceAccountKey.json\n
            7. Place the serviceAccountKey.json file in the root directory of the project."""
            )

        cred = credentials.Certificate(file_path)

        # initialize the app with a service account, granting admin privileges
        firebase_admin.initialize_app(cred, {
            'databaseURL': "https://budining-cf524-default-rtdb.firebaseio.com/"
        })

        # get a reference to the database service
        self.db_ref = db.reference()

# ==============================================================================


    def update_db_data(self, data):
        """Update the nutrition data in firebase database."""
        self.db_ref.update({"Warren": data["warren"], "West": data["west"], "Marciano": data["marciano"], "Granby": data["granby"], "Meta": data["meta"]})

    def get_db_meta(self):
        """Get the metadata from firebase database."""
        return self.db_ref.child("Meta").get()

    def get_warren(self):
        """Get the daily menu from Warren from the Firebase database."""
        return self.db_ref.child("Warren").get()
    def get_west(self):
        """Get the daily menu from West from the Firebase database."""
        return self.db_ref.child("West").get()
    def get_marciano(self):
        """Get the daily menu from Marciano from the Firebase database."""
        return self.db_ref.child("Marciano").get()
    def get_granby(self):
        """Get the daily menu from Granby from the Firebase database."""
        return self.db_ref.child("Granby").get()


# db = FirebaseDB()
# db.update_stock_data({"test": {"test2": "test3"}})
