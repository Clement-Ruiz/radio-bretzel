from datetime import datetime, timedelta
from flask import current_app as app

from docker.errors import NotFound as DockerNotFound

from rb_backend.config import get_config
from rb_backend.channel.source import SourceAbs
from rb_backend.docker import get_docker_client, get_docker_network
from rb_backend.errors import SourceError, SourceNotFound, DockerError
from rb_backend.utils import formats

class DockerSource(SourceAbs):
   """ DockerSource objects represent liquidsoap containers """

   _cached_container = None
   _cached_container_exp = datetime.min

   def __init__(self,
               name,
               **args):
      """ DockerSource constructor. Refer to rb_backend/channel/source/model.py for arguments.
      """
      config = get_config()
      self.name = name
      self._container_name = config['OBJECTS_NAME_PREFIX'] + 'source_' + self.name
      self.stream_mountpoint = args.pop('stream_mountpoint', self.name)

   def create(self, force=False, **args):
      """ Create a source container from given args
      """
      config = get_config()
      docker_client = get_docker_client()
      if self._get_container(cached=False, quiet=True):
         try:
            if not force:
               raise SourceError("container '" + self._container_name + "' already exists. Use force arg to override")
            self.delete(force=True)
         except Exception as e:
            raise SourceError("Couldn't override source : " + str(e))
      _args = formats.get_prefixed_keys(config, 'SOURCE_CONTAINER_').pop('matching')
      _args.update({
         'name': self._container_name,
         'detach': True,
         'read_only': True,
         'environment': {
            'STREAM_HOST': config['STREAM_HOST'],
            'STREAM_SOURCE_PASSWD': config['STREAM_SOURCE_PASSWD'],
            'STREAM_MOUNTPOINT': vars(self).get('stream_mountpoint', self.name)
         }
      })
      image = _args.pop('image', None)
      if not image: raise DockerError('no image name given. Check your configuration')
      try:
         container = docker_client.containers.create(image=image, **_args)
      except Exception as e:
         raise DockerError("Couldn't create source : " + str(e))
      # Handling network connection
      if config['SOURCE_NETWORK']:
         network_config = formats.get_prefixed_keys(config, 'SOURCE_NETWORK_')['matching']
         network_name = config['OBJECTS_NAME_PREFIX'] + network_config.pop('name')
         source_network = get_docker_network(network_name, **network_config)
         try:
            source_network.connect(container)
         except Exception as e:
            self.delete(force=True, quiet=True)
            raise DockerError("Couldn't connect source to sources network : " + stre(e))
      return self

   def _get_container(self, quiet=False, cached=True):
      """ Return source container object and return False if
      doesn't exists
      """
      docker_client = get_docker_client()
      config = get_config()
      if not cached or not self._cached_container_exp > datetime.now(self._cached_container_exp.tzinfo):
         try:
            self._cached_container = docker_client.containers.get(self._container_name)
         except DockerNotFound:
            if quiet:
               self._cached_container = None
               self._cached_container_exp = datetime.min
            else:
               raise SourceNotFound(str(self.name))
         except:
            raise DockerError("couldn't get source container '" + str(self._container_name) + "'")
      # Add config option for following
      self._cached_container_exp = datetime.now() + timedelta(microseconds=1000)
      return self._cached_container

   def start(self, quiet=False):
      container = self._get_container()
      status = container.status
      if status not in ['exited', 'created', 'paused']:
         if status == 'running' and quiet: return self
         raise SourceError("Can't start source in '" + status + "' state")
      try:
         container.start()
      except Exception as e:
         raise DockerError("Couldn't start source : " + str(e))
      return self

   def stop(self, quiet=False):
      container = self._get_container()
      status = container.status
      if status != 'running':
         if quiet: return self
         raise SourceError("Can't stop source in '" + status + "' state")
      try:
         container.stop()
      except Exception as e:
         raise DockeError("Couldn't stop source : " + str(e))
      return self

   @property
   def status(self):
      try:
         container = self._get_container()
      except SourceNotFound:
         return 'non-existent'
      except:
         return 'in error'
      if container.status == 'dead':
         return 'in error'
      if container.status == 'running':
         return 'playing'
      # else container.status is one of 'exited', 'created', 'paused',
      # 'restarting' or 'removing'
      else:
         return 'stopped'

   def delete(self, force=False, quiet=False):
      container = self._get_container(quiet=quiet)
      if quiet:
         self._cached_container = None
         self._cached_container_exp = datetime.min
         return self
      try:
         if container.status in ['running', 'restarting'] and not force:
            raise SourceError("source is playing. Use force arg to force deletion")
         container.remove(force=force)
         self._cached_container = None
         self._cached_container_exp = datetime.min
      except SourceError as e:
         raise e
      except Exception as e:
         raise DockerError("Couldn't delete source : " + str(e))
      return self
