# A file configures application enviroment (env parameter, database....)

import os
WTF_CSRF_ENABLED = True
basedir = os.path.abspath(os.path.dirname(__file__))   #to figure out the path directory

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

# a key used to create cryptographically secure tokens 
# SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
SECRET_KEY = 'LOVE'
# MYCSW_ADMIN = os.environ.get('MYCSW_ADMIN')
MYCSW_ADMIN = 'MYCSW_ADMIN'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_RECORD_QUERIES = True



# class Config:
#     WTF_CSRF_ENABLED = True
#     basedir = os.path.abspath(os.path.dirname(__file__))   #to figure out the path directory

#     SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

#   # a key used to create cryptographically secure tokens 
#     # SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
#     SECRET_KEY = 'LOVE'
#     # MYCSW_ADMIN = os.environ.get('MYCSW_ADMIN')
#     MYCSW_ADMIN = 'MYCSW_ADMIN'
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     SQLALCHEMY_RECORD_QUERIES = True


#     @staticmethod
#     def init_app(app):
#         pass
 


