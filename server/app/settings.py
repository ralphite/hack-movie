#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Ralph<ralph.wen@gmail.com>
# Created on 1/3/17

import os


class Config(object):
    @staticmethod
    def init_app(app):
        pass

    HOST_DOMAIN = os.environ.get('HACKMOVIE_HOST_DOMAIN', '127.0.0.1:5000')

    SECRET_KEY = os.environ.get('HACKMOVIE_FLASK_SECRET', 'flask-app-secret-key')
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    BCRYPT_LOG_ROUNDS = 13

    # Debug Toolbar
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    # SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Caching
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.

    # Mail
    MAILGUN_DOMAIN = os.environ.get('HACKMOVIE_MAILGUN_DOMAIN', 'mailgun-domain')
    MAILGUN_API_KEY = os.environ.get('HACKMOVIE_MAILGUN_API_KEY', 'mailgun-secret-api-key')

    EMAIL_VERIFICATION_TIMEOUT = 3 * 24 * 60 * 60  # 3 days in seconds

    # Webpack
    WEBPACK_MANIFEST_PATH = './static/build/manifest.json'


class ProdConfig(Config):
    ENV = 'prod'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('HACKMOVIE_DB', 'mysql://root@localhost/HACKMOVIE')
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar


class DevConfig(Config):
    ENV = 'dev'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('HACKMOVIE_DB', 'mysql://root@localhost/HACKMOVIE')
    DEBUG_TB_ENABLED = True  # Do not show the debug tool bar for now
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.


class TestConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    BCRYPT_LOG_ROUNDS = 4  # For faster tests; needs at least 4 to avoid "ValueError: Invalid rounds"
    WTF_CSRF_ENABLED = False


settings = {
    'prod': ProdConfig,
    'dev': DevConfig,
    'test': TestConfig,

    'default': DevConfig
}
