#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Ralph<ralph.wen@gmail.com>
# Created on 1/3/17


from flask import jsonify

from . import api

from time import time

from ... import db

from random import sample

from app.models import Movie, Ratings, Links, Rec

from app.utils.poster import get_poster
from app.rec_service.rec import rec_for_movie


def get_movie(movie_id):
    movie = Movie.query.filter_by(movie_id=movie_id).first_or_404()

    link = Links.query.filter_by(movie_id=movie_id).first_or_404()

    res = movie.get_movie()

    res['imdbId'] = link.imdb_id
    res['tmdbId'] = link.tmdb_id

    res['image'] = get_poster(link.tmdb_id)

    return res


@api.route('/get-recommendation/<movie_id>', methods=['GET'])
def get_recommendation(movie_id):

    recs = Rec.query.filter_by(movie_id=movie_id).all()
    movies_ids = [r.rec_movie_id for r in recs]

    if not movies_ids:
        movies_ids = rec_for_movie(movie_id)
        for mid in movies_ids:
            r = Rec()
            r.movie_id = movie_id
            r.rec_movie_id = mid

            db.session.add(r)

        try:
            db.session.commit()
        except:
            db.session.rollback()


    return jsonify({
        'rec_movies': [get_movie(movie_id) for movie_id in movies_ids]
    })

