import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

def initialize_connection():
    cred_obj = firebase_admin.credentials.Certificate(r'C:\Users\apart\Documents\MyFiles\Learn\Git-repositories\RFIDBookLib\RFID\Firebase\rfidbooklib-firebase-adminsdk-gjxai-3c95b75566.json')
    app = firebase_admin.initialize_app(cred_obj, {
        'databaseURL':"https://rfidbooklib-default-rtdb.europe-west1.firebasedatabase.app/"
    })
    return firebase_admin.db, app

def drop_connection(app):
    firebase_admin.delete_app(app)