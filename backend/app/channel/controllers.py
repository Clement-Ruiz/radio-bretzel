from flask import request, abort, jsonify
from flask import current_app as app

from app.channel.models import Channel

from ..channel import channel

@channel.route('/', methods=['POST'])
@channel.route('/<name>', methods=['POST'])
def create_channel():
   name = request.values.get('name')
   if not name:
      abort(400)

   source_container_configuration = {
      # 'volumes': {
      #    app.config['SOURCE_AUDIO_VOLUME_NAME ']:  {
      #       "bind": {
      #          "path": "/audio",
      #          "mode": "ro"
      #       }
      #    }
      # }
   }
   source_container_configuration.update(request.values)
   newChannel = Channel(name, **source_container_configuration)
   return jsonify(str(newChannel._id))
