import os
from app import create_app

env = os.environ.get('RADIO_BRETZEL_ENV', 'development')

app = create_app(env)

params = {
   'host' : '0.0.0.0'
}

if env == 'development':
   params['debug'] = True
   params['use_reloader'] = False
elif env == 'test':
   params['debug'] = True
   params['use_reloader'] = False
else:
   raise ValueError('environment variable not supported ('+ env + ')')

if __name__ == '__main__':
   app.run(**params)
