#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Ralph<ralph.wen@gmail.com>
# Created on 1/3/17


from flask import jsonify

from . import api

from time import time

from ... import db

from app.models import Movie, Ratings


@api.route('/rating/<user_id>/<movie_id>', methods=['GET'])
def get_rating(user_id, movie_id):
    rating = Ratings.query.filter_by(user_id=user_id).filter_by(movie_id=movie_id).first_or_404()

    return jsonify(rating.get_rating())


@api.route('/ratings', methods=['GET'])
def get_all_ratings():
    ratings = Ratings.query.all()

    return jsonify({
        'ratings': [r.get_rating() for r in ratings]
    })


@api.route('/rating/<user_id>/<movie_id>/<rate>', methods=['POST'])
def rate(user_id, movie_id, rate):
    ratings = Ratings()
    ratings.user_id = user_id
    ratings.movie_id = movie_id
    ratings.rating = rate
    ratings.timestamp = str(int(time()))

    try:
        db.session.add(ratings)
        db.session.commit()
        return jsonify({
            'message': 'successful'
        }), 200
    except:
        db.session.rollback()
        return jsonify({
            'message': 'failed'
        }), 500
