import os

DATABASE_NAME = os.environ['DATABASE_NAME']
DATABASE_USER = os.environ['DATABASE_USER']
DATABASE_PASSWORD = os.environ['DATABASE_PASSWORD']
if DATABASE_USER == 'root':
    DATABASE_PORT = 3307
else:
    DATABASE_PORT = 3306

DATABASE_URI = 'mysql+pymysql://{}:{}@localhost:{}/{}'.format(
    DATABASE_USER,
    DATABASE_PASSWORD,
    DATABASE_PORT,
    DATABASE_NAME
)
