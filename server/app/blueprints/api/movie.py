#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Ralph<ralph.wen@gmail.com>
# Created on 1/3/17


from flask import jsonify

from . import api

from app.models import Movie, Links

from app.utils.poster import get_poster


@api.route('/movie/<movie_id>', methods=['GET'])
def get_movie(movie_id):
    movie = Movie.query.filter_by(movie_id=movie_id).first_or_404()

    link = Links.query.filter_by(movie_id=movie_id).first_or_404()

    res = movie.get_movie()

    res['imdbId'] = link.imdb_id
    res['tmdbId'] = link.tmdb_id

    res['image'] = get_poster(link.tmdb_id)

    return jsonify(res)


@api.route('/movies', methods=['GET'])
def get_all_movies():
    movies = Movie.query.all()

    return jsonify({
        'movies': [m.get_movie() for m in movies]
    })
