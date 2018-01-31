import os
from random import randint

from app import db, docker, config

class Channel(object):

   def __init__(self, name, **dockerArgs):
      self.name = name
      conf = config['SOURCE']['CONTAINER_ARGS']
      conf.update(dockerArgs)
      source = docker.container.create(name = name, conf)
      if not source:
          raise SystemError('Failed to create source container')
      self.source = source
      return source
