from flask_pymongo import PyMongo

def connect_db(app):
   """ Open a Mongodb connection."""
   client = PyMongo(app)
   return client

def init_db(app):
   """ Initiate DB connection at app startup """
   if not hasattr(app, 'database'):
      app.mongo = connect_db(app)
   return app
