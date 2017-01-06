#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Ralph<ralph.wen@gmail.com>
# Created on 1/3/17

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.bcrypt import Bcrypt
from flask.ext.cache import Cache
from flask.ext.debugtoolbar import DebugToolbarExtension
# from flask.ext.webpack import Webpack
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView
from flask_cors import CORS, cross_origin

from settings import settings

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.session_protection = 'basic'
login_manager.login_view = 'auth.login'

bcrypt = Bcrypt()
cache = Cache()
debug_toolbar = DebugToolbarExtension()
# webpack = Webpack()


def create_app(config_type):
    app = Flask(__name__)

    CORS(app)

    config = settings[config_type]
    app.config.from_object(config)
    config.init_app(app)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    cache.init_app(app)
    debug_toolbar.init_app(app)
    # webpack.init_app(app)

    admin = Admin(app, name='HACKMOVIE', template_mode='bootstrap3')

    # from models import Problem, Tag, Album, Company
    #
    # admin.add_view(ModelView(Problem, db.session))
    # admin.add_view(ModelView(Album, db.session))
    # admin.add_view(ModelView(Tag, db.session))
    # admin.add_view(ModelView(Company, db.session))

    _register_blueprints(app)

    return app


def _register_blueprints(app):
    from .blueprints.main import main as main_blueprint
    from .blueprints.api import api as api_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(api_blueprint, url_prefix='/api')