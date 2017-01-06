#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Ralph<ralph.wen@gmail.com>
# Created on 1/3/17


from flask import jsonify

from . import api
from app import db

from app.models import Movie, Links, Rec

from app.utils.poster import get_poster
from app.rec_service.rec import rec_for_movie

from app.decorators import jsonp


@api.route('/movie/<movie_id>', methods=['GET'])
def get_movie(movie_id):
    movie = Movie.query.filter_by(movie_id=movie_id).first_or_404()

    link = Links.query.filter_by(movie_id=movie_id).first_or_404()

    res = movie.get_movie()

    res['imdbId'] = link.imdb_id
    res['tmdbId'] = link.tmdb_id

    if not res['poster']:
        res['poster'] = get_poster(link.tmdb_id)

        movie.poster = res['poster']

        db.session.add(movie)
        try:
            db.session.commit()
        except:
            db.session.rollback()

    recs = Rec.query.filter_by(movie_id=movie_id).all()

    if not recs:
        rec_ids = rec_for_movie(int(movie_id))
        for rec_id in rec_ids:
            r = Rec()
            r.movie_id = movie.movie_id
            r.rec_movie_id = rec_id
            db.session.add(r)

        try:
            db.session.commit()
        except:
            db.session.rollback()
        recs = Rec.query.filter_by(movie_id=movie_id).all()

    res['recs'] = [r.rec_movie_id for r in recs]

    return jsonify(res)


@jsonp
@api.route('/movie-jsonp/<movie_id>', methods=['GET'])
def get_movie(movie_id):
    movie = Movie.query.filter_by(movie_id=movie_id).first_or_404()

    link = Links.query.filter_by(movie_id=movie_id).first_or_404()

    res = movie.get_movie()

    res['imdbId'] = link.imdb_id
    res['tmdbId'] = link.tmdb_id

    if not res['poster']:
        res['poster'] = get_poster(link.tmdb_id)

        movie.poster = res['poster']

        db.session.add(movie)
        try:
            db.session.commit()
        except:
            db.session.rollback()

    recs = Rec.query.filter_by(movie_id=movie_id).all()

    if not recs:
        rec_ids = rec_for_movie(int(movie_id))
        for rec_id in rec_ids:
            r = Rec()
            r.movie_id = movie.movie_id
            r.rec_movie_id = rec_id
            db.session.add(r)

        try:
            db.session.commit()
        except:
            db.session.rollback()
        recs = Rec.query.filter_by(movie_id=movie_id).all()

    res['recs'] = [r.rec_movie_id for r in recs]

    return jsonify(res)


@api.route('/movies', methods=['GET'])
def get_all_movies():
    movies = Movie.query.all()

    return jsonify({
        'movies': [m.get_movie() for m in movies]
    })
