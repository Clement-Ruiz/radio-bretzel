from flask import Flask, jsonify
from flask_pymongo import PyMongo

from app import docker, config

def start():
   """ Main application entry point """
   app = Flask(__name__)

   load_config(app)
   register_modules(app)

   @app.route('/')
   def hello_world():
      return 'Welcome to Radio Bretzel'

   # @app.route('/new', methods=['GET','POST'])
   # def new():
   #    newSource = source.create('test_source-creation')
   #    return newSource.id
   #
   # @app.route('/next')
   # def next():
   #    return SourceModels.select_next_track()

   @app.route('/config')
   def get_config():
      return jsonify(rbConfig)

   @app.route('/docker')
   def get_docker():
      return jsonify(app.docker.info())

   return app

def load_config(app):
    rbConfig = config.load()
    app.config.update(rbConfig)

def register_modules(app):
   """Activate Flask extensions and initiate external connections"""
   PyMongo(app)
   docker.init_app(app)
