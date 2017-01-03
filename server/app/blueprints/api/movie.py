#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Ralph<ralph.wen@gmail.com>
# Created on 1/3/17


from flask import jsonify

from . import api

from app.models import Movie


@api.route('/movie/<movie_id>', methods=['GET'])
def get_movie(movie_id):
    movie = Movie.query.filter_by(movie_id=movie_id).first_or_404()

    return jsonify(movie.get_movie())
