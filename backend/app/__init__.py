from flask import Flask, jsonify

from app import docker
from app.database import db
from app.config import load

def start():
   """ Main application entry point """
   app = Flask(__name__)

   rbConfig = load()
   app.config.update(rbConfig)

   register_modules(app)

   @app.route('/')
   def hello_world():
      return 'Welcome to Radio Bretzel'

   # @app.route('/new', methods=['GET','POST'])
   # def new():
   #       newSource = source.create('test_source-creation')
   #       return newSource.id
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


def register_modules(app):
    """Activate Flask extensions and initiate external connections"""
    # db.init_app(app)
    docker.init_app(app)
