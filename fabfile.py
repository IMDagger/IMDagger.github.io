from fabric.api import *
import fabric.contrib.project as project
import os
import datetime

# Local path configuration (can be absolute or relative to fabfile)
env.deploy_path = 'output'
SRC_PATH = env.deploy_path

# Remote server configuration
production = 'root@localhost:22'
dst_path = 'deploy/'

# Rackspace Cloud Files configuration settings
env.cloudfiles_username = 'my_rackspace_username'
env.cloudfiles_api_key = 'my_rackspace_api_key'
env.cloudfiles_container = 'my_cloudfiles_container'


def clean():
    if os.path.isdir(SRC_PATH):
        local('rm -rf {deploy_path}'.format(**env))
        local('mkdir {deploy_path}'.format(**env))

def build():
    local('pelican -s pelicanconf.py')

def rebuild():
    clean()
    build()

def regenerate():
    local('pelican -r -s pelicanconf.py')

def serve():
    local('cd {deploy_path} && python -m SimpleHTTPServer'.format(**env))

def reserve():
    build()
    serve()

def preview():
    local('pelican -s publishconf.py')

def cf_upload():
    rebuild()
    local('cd {deploy_path} && '
          'swift -v -A https://auth.api.rackspacecloud.com/v1.0 '
          '-U {cloudfiles_username} '
          '-K {cloudfiles_api_key} '
          'upload -c {cloudfiles_container} .'.format(**env))

def publish(dst_path=dst_path):
    local('pelican -s publishconf.py')
    exclude = ' '.join('--exclude ' + fname for fname in ['.DS_Store', '.git', 'README.md', 'LICENSE'])
    normal = lambda x: (x.rstrip('/') + '/')
    local('rsync -r {0} --delete {src} {dst}'.format(exclude, src=normal(SRC_PATH), dst=normal(dst_path)))
    local('cd {0} && git add . && git commit -a -m "snapshot {1}"'.format(normal(dst_path), datetime.datetime.now().isoformat()))
