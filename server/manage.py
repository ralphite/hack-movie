#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Ralph<ralph.wen@gmail.com>
# Created on 12/31/16

import os

basedir = os.path.abspath(os.path.dirname(__file__))

# import configuration from .env file.
SECRETS_ENV_FILE_NAME = '.secrets.env'
SECRETS_ENV_FILE = os.path.abspath((os.path.join(basedir, SECRETS_ENV_FILE_NAME)))

if os.path.exists(SECRETS_ENV_FILE):
    print 'Importing environment variables from ' + SECRETS_ENV_FILE_NAME + '...'
    for line in open(SECRETS_ENV_FILE):
        name, value = line.strip().split('=')
        print '  + ' + name.ljust(30, ' ') + ': ' + value
        os.environ[name] = value
    print '-' * 50

from app import create_app, db
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

app = create_app(os.getenv('WEB_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
