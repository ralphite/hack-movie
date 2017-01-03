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


@manager.command
def populate_data():
    from app.models import Movie, Links, Ratings, Tags

    with(open('./data/movies.csv', 'r')) as movie_data:
        for line in movie_data:
            if not line[:7] == 'movieId':
                # movieId,title,genres
                # 2,Jumanji (1995),Adventure|Children|Fantasy
                line = line.strip()
                movie = Movie()
                print line
                first_index = line.find(',')
                last_index = line.rfind(',')
                movie.movie_id, movie.title, movie.genres = line[:first_index], line[first_index + 1:last_index], line[last_index + 1:]
                db.session.add(movie)
        db.session.commit()


if __name__ == '__main__':
    manager.run()
