#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Ralph<ralph.wen@gmail.com>
# Created on 1/3/17

from flask import Blueprint

main = Blueprint('main', __name__)

from . import views
