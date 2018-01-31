import json, os

def load(*env):
   authorizedEnv = [
      'development',
      'test',
      # 'production'
   ]
   if not env:
      env = os.environ.get('RADIOBRETZEL_BACKEND_ENV', 'development')
   if not env in authorizedEnv:
      raise ValueError('Invalid environment name')
      return False

   base_dir = os.path.dirname(__file__)


   config = json.load(open(base_dir + '/default.json'))
   rbEnvConfig = json.load(open(base_dir + '/' + env + ".json"))
   rbLocalConfig = json.load(open(base_dir + '/local.json'))

   config.update(rbEnvConfig)
   config.update(rbLocalConfig)

   return config
