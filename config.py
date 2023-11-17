from os import path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    STATIC_URL = 'static'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(basedir, 'webml.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
