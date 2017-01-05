#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Ralph<ralph.wen@gmail.com>
# Created on 1/3/17


from flask import jsonify

from . import api

from time import time

from ... import db

from random import sample

from app.models import Movie, Ratings


def get_rec_movies(user_id):
    movies = Movie.query.all()

    return [m.movie_id for m in sample(movies, 5)]


@api.route('/get-recommendation/<user_id>', methods=['GET'])
def get_recommendation(user_id):
    movies_ids = get_rec_movies(user_id)

    return jsonify({
        'rec_movies': movies_ids
    })
