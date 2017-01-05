#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Ralph<ralph.wen@gmail.com>
# Created on 1/5/17


import MySQLdb
import pandas as pd
import numpy as np

mysql_cn = MySQLdb.connect(
    host='localhost',
    port=3306, user='root', passwd='',
    db='HACKMOVIE'
)

users = pd.read_sql('select * from users;', con=mysql_cn)
movies = pd.read_sql('select * from movies;', con=mysql_cn)
tags = pd.read_sql('select * from tags;', con=mysql_cn)
ratings = pd.read_sql('select * from ratings;', con=mysql_cn)
links = pd.read_sql('select * from links;', con=mysql_cn)

mysql_cn.close()

print '#' * 100
print 'Padas dataframes loaded from MySQL...'

data = pd.merge(ratings, movies, on='movie_id')
# data = ratings
data = data.convert_objects(convert_numeric=True)

pt = data.pivot_table(index=['user_id'], columns=['movie_id'], values=['rating'])
pt.columns = pt.columns.droplevel(0)


def rec_for_movie(movie_id):
    provided_movie_ratings = pt[movie_id]

    similar_movies = pt.corrwith(provided_movie_ratings)
    similar_movies = similar_movies.dropna()
    similar_movies = pd.DataFrame(similar_movies.sort_values(ascending=False))

    groupby_data = data[['movie_id', 'rating']].groupby(['movie_id']).agg(['std', 'mean', 'count'])

    groupby_data.columns = groupby_data.columns.droplevel(0)
    a = groupby_data['count'] > 50
    b = groupby_data[a]

    sim_100_mov = b.join(similar_movies)
    sim_100_mov.columns = ['count', 'mean', 'std', 'similarity']
    sim_100_mov = sim_100_mov.sort_values('similarity', ascending=False)

    print sim_100_mov

rec_for_movie(13)