#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Ralph<ralph.wen@gmail.com>
# Created on 1/3/17

from datetime import datetime

from . import db


class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return self.userid


class Movie(db.Model):
    __tablename__ = 'movies'

    movie_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.UnicodeText)
    genres = db.Column(db.UnicodeText)

    def get_movie(self):
        return {
            'movieId': self.movie_id,
            'title': self.title,
            'genres': self.genres
        }

    def __repr__(self):
        return self.title


class Ratings(db.Model):
    __tablename__ = 'ratings'

    user_id = db.Column(db.ForeignKey('users.user_id'), nullable=False, primary_key=True)
    movie_id = db.Column(db.ForeignKey('movies.movie_id'), nullable=False, primary_key=True)
    rating = db.Column(db.String(100))
    timestamp = db.Column(db.String(100))

    def get_rating(self):
        return {
            'userId': self.user_id,
            'movieId': self.movie_id,
            'rating': self.rating,
            'timestamp': self.timestamp
        }

    def __repr__(self):
        return self.rating


class Tags(db.Model):
    __tablename__ = 'tags'

    user_id = db.Column(db.ForeignKey('users.user_id'), nullable=False, primary_key=True)
    movie_id = db.Column(db.ForeignKey('movies.movie_id'), nullable=False, primary_key=True)
    tag = db.Column(db.String(100))
    timestamp = db.Column(db.String(100))

    def get_rating(self):
        return {
            'userId': self.user_id,
            'movieId': self.movie_id,
            'tag': self.tag,
            'timestamp': self.timestamp
        }

    def __repr__(self):
        return self.tag


class Links(db.Model):
    __tablename__ = 'links'

    movie_id = db.Column(db.ForeignKey('movies.movie_id'), nullable=False, primary_key=True)
    imdb_id = db.Column(db.String(100))
    tmdb_id = db.Column(db.String(100))

    def get_rating(self):
        return {
            'movieId': self.movie_id,
            'imdbId': self.imdb_id,
            'tmdbId': self.tmdb_id
        }
