import json, os

def load():
   authorizedEnv = [
      'development',
      'test',
      # 'production'
   ]
   env = os.environ.get('RADIO_BRETZEL_ENVIRONMENT', 'development')
   if env and not env in authorizedEnv:
      raise ValueError('Invalid environment name')
      return False

   base_dir = os.path.dirname(__file__)

   config = json.load(open(base_dir + '/default.json'))
   rbEnvConfig = json.load(open(base_dir + '/' + env + '.json'))
   rbLocalConfig = json.load(open(base_dir + '/local.json'))

   config.update(rbEnvConfig)
   config.update(rbLocalConfig)

   return config
