import docker

_con = None

def client(config):
   global _con
   if not _con:
      _con = docker.DockerClient(
         base_url=config["DOCKER_URL"],
         version=config["DOCKER_VERSION"]
      )
   return _con

def init_app(app):
    global _con
    if not _con:
       client(app.config)

    app.docker = _con
    return app
    #_con.volumes.create(name="radiobretzel-db", config.DOCKER_VOLUME_OPTS)
