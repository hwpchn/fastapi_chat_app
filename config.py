import configparser

# 读取配置文件
config = configparser.ConfigParser()
config.read('config.ini')

# 提取配置信息
SECRET_KEY = config.get('JWT', 'SECRET_KEY')
ALGORITHM = config.get('JWT', 'ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = config.getint('JWT', 'ACCESS_TOKEN_EXPIRE_MINUTES')
DATABASE_NAME = config.get('DEFAULT', 'DATABASE_NAME')
FRIEND_REQUEST_EXPIRY_DAYS = config.getint('FRIEND_REQUEST', 'EXPIRY_DAYS')

