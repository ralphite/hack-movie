#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Ralph<ralph.wen@gmail.com>
# Created on 1/3/17

import base64

from datetime import datetime

from flask.ext.login import UserMixin

from . import db, login_manager, bcrypt


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key=True)

    weibo_id = db.Column(db.String(20), unique=True, index=True)
    wechat_id = db.Column(db.String(20), unique=True, index=True)

    email = db.Column(db.String(100), unique=True, index=True)
    email_verified = db.Column(db.Boolean, server_default='0')
    password = db.Column(db.String(100))

    username = db.Column(db.Unicode(100), unique=True, index=True)
    name = db.Column(db.Unicode(100))
    bio = db.Column(db.UnicodeText)
    avatar_url = db.Column(db.String(500))

    emailVerifications = db.relationship('EmailVerification', backref='user')

    def get_id(self):
        return self.user_id

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        if not self.password:
            return password == ''
        return bcrypt.check_password_hash(self.password, password)

    def to_json(self):
        return {
            'id': self.user_id,
            'email': self.email,
            'username': self.username,
            'name': self.name,
            'bio': self.bio,
            'avatar_url': self.avatar_url
        }

    def __repr__(self):
        return self.email


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class EmailVerification(db.Model):
    __tablename__ = 'email_verification'

    guid = db.Column(db.String(100), primary_key=True)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now())
    verified_time = db.Column(db.DateTime, nullable=True)
    user_id = db.Column(db.ForeignKey('user.user_id'), nullable=False)

    def __repr__(self):
        return self.guid[:7]


class Problem(db.Model):
    __tablename__ = 'problem'

    problem_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.UnicodeText)
    level = db.Column(db.Integer)

    LEVELS = {
        0: "Very Easy",
        1: "Easy",
        2: "Medium",
        3: "Hard",
        4: "Very Hard"
    }

    @staticmethod
    def encode_content(content):
        return base64.encodestring(content)

    @staticmethod
    def decode_content(content):
        return base64.decodestring(content)

    def get_problem(self):
        return {
            'id': self.problem_id,
            'title': self.title,
            'description': self.description,
            'level': self.level and self.LEVELS[self.level] or '',
            'tags': [tag.name for tag in self.tags],
            'companies': [company.name for company in self.companies],
        }

    def __repr__(self):
        return self.title
