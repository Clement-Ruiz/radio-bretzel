#   Default configuration file.
#
#   This configuration will be merged with the corresponding environment
#   configuration. Any parameter described in one of the environment
#   configurations files will prevail on those described bellow. Following
#   content will be overriden if explicited through the different files in
#   this folder.
#
#   /!\
#               This file should not be edited by anyone except Radio
#               Bretzel development team.
#                                                                          /!\

class Default(object):

   NAME = 'RadioBretzel'
   OBJECTS_NAME_PREFIX = 'rb_'

   DOCKER_URL = 'unix://var/run/docker.sock'
   DOCKER_VERSION = 'auto'

   MONGO_HOST = 'mongo.rb_default'
   MONGO_DBNAME = 'radiobretzel'

   SOURCE_CONTAINER_IMAGE = 'radiobretzel/source:latest'
   SOURCE_CONTAINER_AUDIO_VOLUME = 'radiobretzel_audio'
   SOURCE_NETWORK = 'default'

class Development(object):

   DEBUG = True
   ASSETS_DEBUG = True
   WTF_CSRF_ENABLED = False

   SOURCE_CONTAINER_IMAGE = 'radiobretzel/source:dev'

class Test(object):

   TESTING =  True
   WTF_CSRF_ENABLED =  False
