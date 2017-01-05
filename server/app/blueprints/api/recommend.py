#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Ralph<ralph.wen@gmail.com>
# Created on 1/3/17


from flask import jsonify

from . import api

from time import time

from ... import db

from random import sample

from app.models import Movie, Ratings, Links


def get_rec_movies(movie_id):
    movies = Movie.query.all()

    return [m.movie_id for m in sample(movies, 5)]


def get_movie(movie_id):
    movie = Movie.query.filter_by(movie_id=movie_id).first_or_404()

    link = Links.query.filter_by(movie_id=movie_id).first_or_404()

    res = movie.get_movie()

    res['imdbId'] = link.imdb_id
    res['tmdbId'] = link.tmdb_id

    return res


@api.route('/get-recommendation/<movie_id>', methods=['GET'])
def get_recommendation(movie_id):
    movies_ids = get_rec_movies(movie_id)

    return jsonify({
        'rec_movies': [get_movie(movie_id) for movie_id in movies_ids]
    })
