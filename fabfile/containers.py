#!/usr/bin/env python

import string

from load_config import configuration
from fabric.api import task, run, cd, roles

import vault

build_config = configuration['build']
run_config = configuration['run']


@roles('flowercluster')
@task
def start_all():
    """ Start all containers in config.yml during a deploy. """

    for config in run_config:
        print('starting ' + config['name'])
        _run_start(config)


@roles('flowercluster')
@task
def start(name):
    """ Initialize all containers matching a name. """

    for config in [u for u in run_config if u['name'] == name]:
        _run_start(config)


def _run_start(config):
    """ Initialize a container with a SecretID token.  """

    if 'cmd' in config:
        cmd = [config['cmd'], vault.secret_id(config['approle'])]
        run(string.join(cmd))

    if 'unit' in config:
        run('sudo systemctl restart ' + config['unit'])


@roles('flowercluster')
@task
def build_all():
    """ Build all images specified in config.yml """

    for config in build_config:
        _run_build(config)


@roles('flowercluster')
@task
def build(name):
    """ Build all images matching a name. """

    for config in [i for i in build_config if i['name'] == name]:
        _run_build(config)


def _run_build(config):
    """ Run the docker command to build an image, using its configuration
    from config.yml.
    """

    args = [
        'docker build . -t {}'.format(config['name']),
    ]

    if 'approle' in config:
        # append vault RoleID credentials
        args.append('--build-arg ROLE_ID=' + vault.role_id(config['approle']))

    with cd(config['path']):
        run(string.join(args))


__all__ = ['build', 'build_all', 'start', 'start_all']
