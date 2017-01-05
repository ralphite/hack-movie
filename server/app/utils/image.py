#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Ralph<ralph.wen@gmail.com>
# Created on 1/5/17

import requests

import json

# https://api.themoviedb.org/3/movie/11962/images?api_key=0a6cdcc6768de0322e08e5a73fe18108&language=en-US&include_image_language=en,null

def get_poster(imdbId):
    url = 'https://api.themoviedb.org/3/movie/' + imdbId + '/images?api_key=0a6cdcc6768de0322e08e5a73fe18108&language=en-US&include_image_language=en,null'

    try:
        content = requests.get(url).content
        res = json.loads(content)['posters']

        if not res:
            return ''

        return res[0]['file_path']
    except:
        return ''