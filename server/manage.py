#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Ralph<ralph.wen@gmail.com>
# Created on 12/31/16

import os

from app.rec_service import rec
from app.utils.poster import get_poster
from app.models import Movie, Links, Ratings, Tags, User, Rec

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
    with(open('./data/movies.csv', 'r')) as movie_data:
        for line in movie_data:
            if not line[:7] == 'movieId':
                # movieId,title,genres
                # 2,Jumanji (1995),Adventure|Children|Fantasy
                line = line.strip()
                movie = Movie()
                first_index = line.find(',')
                last_index = line.rfind(',')
                movie.movie_id, movie.title, movie.genres = \
                    line[:first_index], line[first_index + 1:last_index], line[last_index + 1:]
                db.session.add(movie)
        db.session.commit()

    with(open('./data/links.csv', 'r')) as links_data:
        for line in links_data:
            if not line[:7] == 'movieId':
                # movieId,imdbId,tmdbId
                # 1,0114709,862
                line = line.strip()
                link = Links()
                link.movie_id, link.imdb_id, link.tmdb_id = line.split(',')
                db.session.add(link)
        db.session.commit()

    for user_id in xrange(1, 672):
        user = User()
        user.user_id = user_id
        db.session.add(user)
    db.session.commit()

    with(open('./data/tags.csv', 'r')) as tags_data:
        for line in tags_data:
            if not line[:6] == 'userId':
                # userId,movieId,tag,timestamp
                # 15,339,sandra 'boring' bullock,1138537770
                line = line.strip()
                tag = Tags()
                arr = line.split(',')
                tag.user_id, tag.movie_id = arr[:2]
                tag.timestamp = arr[-1]
                tag.tag = ','.join(arr[2:-1])
                db.session.add(tag)
        db.session.commit()

    with(open('./data/ratings.csv', 'r')) as ratings_data:
        for line in ratings_data:
            if not line[:6] == 'userId':
                # userId,movieId,rating,timestamp
                # 1,31,2.5,1260759144
                line = line.strip()
                rating = Ratings()
                rating.user_id, rating.movie_id, rating.rating, rating.timestamp = line.split(',')
                db.session.add(rating)
        db.session.commit()


@manager.command
def add_posters():

    movies = Movie.query.all()

    for movie in movies[:1000]:
        link = Links.query.filter_by(movie_id=movie.movie_id).first_or_404()
        movie.poster = get_poster(link.tmdb_id)

        db.session.add(movie)

    try:
        db.session.commit()
    except:
        db.session.rollback()


@manager.command
def add_rec():
    movies = Movie.query.all()
    movies = [m for m in movies if m.poster]

    for movie in movies:
        rec_ids = rec.rec_for_movie(movie.movie_id)

        for rec_id in rec_ids:
            r = Rec()
            r.movie_id = movie.movie_id
            r.rec_movie_id = rec_id
            db.session.add(r)

        try:
            db.session.commit()
        except:
            db.session.rollback()

if __name__ == '__main__':
    manager.run()
