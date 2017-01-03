#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Ralph<ralph.wen@gmail.com>
# Created on 12/31/16


from fabric.api import local, run, env, cd, get, put

env.hosts = ['54.68.154.137'] 
env.user = 'ec2-user'
env.key_filename = '../hack-movie.pem'

remote_project_folder = '/home/ec2-user/hack-movie/src/site'

local_assets_folder = './app/assets'


def dev():
    local('cd ' + local_assets_folder + '; npm run dev &')
    local('python manage.py runserver -r -d')


def prod():
    local('WEB_CONFIG=prod python manage.py runserver -r')


def deploy_server():
    with cd(remote_project_folder):
        run('git pull')
        run('touch manage.py')


def deploy_assets():
    build_assets()
    upload_assets()
    list_assets()


def fetch_remote_logs():
    get(remote_path=remote_project_folder + '/access.log', local_path='./access_server.log')
    get(remote_path=remote_project_folder + '/error.log', local_path='./error_server.log')


def build_assets():
    local('rm -fr ./app/static/build')
    local('cd ' + local_assets_folder + '; npm run build')


def upload_assets():
    run('rm -fr ' + remote_project_folder + '/app/static/build')
    put(local_path='./app/static/build', remote_path=remote_project_folder + '/app/static')


def list_assets():
    run('ls -lR ' + remote_project_folder + '/app/static/build')


def deploy_nginx():
    pass


def renew_ssl():
    pass
