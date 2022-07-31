import os
from datetime import timedelta
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = False
    SECRET_KEY = os.environ["SECRET_KEY"]
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
    JWT_COOKIE_SECURE = False
    JWT_COOKIE_CSRF_PROTECT = False  # True in production, only due to Nuxt-auth calamity
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=14)


class ProductionConfig(Config):
    DEBUG = False
    # JWT_COOKIE_SECURE = True  # only over https


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
