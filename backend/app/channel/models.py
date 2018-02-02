import os, re
from random import randint
from flask import current_app as app

from app import utils


class Channel(object):

   def __init__(self, _id, **dockerArgs):
      args = {}
      args['name'] = _id
      args.update(**dockerArgs)
      if self.validate(**args):
         self._id = _id
         self.source = self.create_source(_id, **dockerArgs)
         self.save()
      else:
         raise ValueError("Couldn't create Channel - wrong parameter detected")


   def create_source(self,
               name,
               # volumes={
               #    'radiobretzel_audio': {
               #       "bind": {
               #          "path": "/audio",
               #          "mode": "ro"
               #       }
               #    }
               # },
               **dockerArgs):
      """ Create a source container from given args """

      conf = dockerArgs
      default = {
         'detach': True,
         'read_only': True,
         'network': app.config['OBJECTS_NAME_PREFIX'] + app.config['SOURCE_NETWORK'],
         'auto_remove': True
      }

      # "volumes": {
      #    utils.prefix(config['SOURCE_AUDIO_VOLUME_NAME']): {

      #    }
      # }
      conf.update(default)
      if dockerArgs.get('image'):
         image = dockerArgs['image']
      else:
         image = app.config['SOURCE_CONTAINER_IMAGE']
      conf['name'] = app.config['OBJECTS_NAME_PREFIX'] + name

      source = app.docker.containers.run(image=image, **conf)
      if not source:
         raise SystemError('Failed to create source container')
      return source

   def save(self):
      data = {
         '_id': self._id,
         'source': self.source.name
      }
      if app.mongo.db.sources.insert_one(data):
         return True

   def reload_source(self):
      return True

   def validate(self, **data):
      for field in data:
         if field == 'name':
            if not data[field] or not utils.validate_slug(data[field]):
               return False #'Attribute name don\'t fit the requirements.'
      return True
