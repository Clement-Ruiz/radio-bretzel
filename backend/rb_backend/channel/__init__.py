import random

from flask import request, abort

from rb_backend.channel.model import Channel, Channels
from rb_backend.channel import view
from rb_backend.errors import DatabaseError, ValidationError
from rb_backend.source import Sources
from rb_backend.utils import formats, validations

def routes(app):
   """ All routes for channel resources"""

   @app.route('/channel/', methods=['GET'])
   def get_channels():
      values = request.args.to_dict()
      channels = Channels.find(**values)
      return view.many(*channels)

   @app.route('/channel/<string:slug>', methods=['GET'])
   def get_channel(slug):
      values = request.args.to_dict()
      values.update({'slug': slug})
      channel = Channels.find_one(**values)
      return view.one(channel)

   @app.route('/channel/<string:slug>', methods=['POST'])
   def create_channel(slug):
      values = request.form.to_dict()
      values.update({'slug': slug})
      channel = Channels.create(**values)
      return view.one(channel)

   @app.route('/channel/<string:slug>', methods=['PUT', 'UPDATE'])
   def update_channel(slug):
      values = request.form.to_dict()
      updated_channel = Channels.update(slug, values)
      return view.one(update_channel)

   @app.route('/channel/<string:slug>', methods=['DELETE'])
   def delete_channel(slug):
      values = request.form.to_dict()
      deleted_channel = Channels.delete(slug, **values)
      return view.one(deleted_channel)
