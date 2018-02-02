import docker

def connect_docker(config):
   client = docker.DockerClient(
      base_url=config["url"],
      version=config["version"]
   )
   return client

def init_docker(app):
   if not hasattr(app, 'docker'):
      app.docker = connect_docker(app.config.get_namespace('DOCKER_'))
   app.source_network = get_source_network(app)
   return app

def get_source_network(app):
   network_config = app.config.get_namespace('SOURCE_NETWORK_')
   network_name = app.config['OBJECTS_NAME_PREFIX'] + app.config['SOURCE_NETWORK']
   if not hasattr(app, 'source_network'):
      print("Passing in network creation")
      app.source_network = app.docker.networks.create(network_name, **network_config)
   return app.source_network
