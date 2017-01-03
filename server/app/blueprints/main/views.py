#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Ralph<ralph.wen@gmail.com>
# Created on 1/3/17

from flask import render_template, send_from_directory, current_app, request, json

from . import main


@main.route('/robots.txt')
def robots():
    return send_from_directory(current_app.static_folder, request.path[1:])


@main.route('/')
def index():
    return render_template('index.html')