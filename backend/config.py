import os
SECRET_KEY = os.urandom(32)

# IMPLEMENT DATABASE URL
DATABASE_NAME = 'trivia'
SQLALCHEMY_DATABASE_URI = 'postgresql://{}/{}'.format('postgres:abc@localhost:5432', DATABASE_NAME)
SQLALCHEMY_TRACK_MODIFICATIONS = False
