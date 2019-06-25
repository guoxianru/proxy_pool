# database config
from os import getenv


class ConfigError(BaseException):
    pass


DB_TYPE = getenv('db_type', 'SSDB')

if DB_TYPE == 'SSDB':
    DB_HOST = getenv('ssdb_host', '127.0.0.1')
    DB_PORT = getenv('ssdb_port', '6379')
elif DB_TYPE == 'MONGODB':
    DB_HOST = getenv('mongodb_host', '127.0.0.1')
    DB_PORT = getenv('mongodb_host', '27017')
else:
    raise ConfigError('Unknown database type, your environment variable `db_type` should be one of SSDB/MONGODB.')

DATABASES = {
    "default": {
        # TYPE SSDB/MONGODB if use redis, only modify the host port, the type should be SSDB
        "TYPE": "SSDB",
        "HOST": "39.106.189.108",
        "PORT": 6379,
        "NAME": "proxy",
        "PASSWORD": "1111"

    }
}

# register the proxy getter function

PROXY_GETTER = [
    'freeProxy_iphai',
    'freeProxy_89',
    'freeProxy_kuai',
    'freeProxy_yun',
    'freeProxy_xici',
    'freeProxy_xila',
    'freeProxy_qiyun',
    'freeProxy_nima',
    'freeProxy_shengji',
    'freeProxy_xiaoshu',
    'freeProxy_proxylistplus',
]

# # API config http://127.0.0.1:5010

SERVER_API = {
    # The ip specified which starting the web API
    "HOST": "0.0.0.0",
    # port number to which the server listens to
    "PORT": 5010
}
