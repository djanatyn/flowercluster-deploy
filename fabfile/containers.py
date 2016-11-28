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
    """ Start all units in config.yml during a deploy. """

    for config in run_config:
        print('starting ' + config['name'])
        _run_start(config)


@roles('flowercluster')
@task
def start(name):
    """ Start all units matching a name. """

    for config in [u for u in run_config if u['name'] == name]:
        _run_start(config)


def _run_start(config):
    """ Start a systemd unit to get a container running.
    Returns whether the start was successful.
    """

    start = run('sudo systemctl start ' + config['unit'])
    return start.succeeded


@roles('flowercluster')
@task
def build_all():
    """ Build all containers specified in config.yml """

    for config in build_config:
        _run_build(config)


@roles('flowercluster')
@task
def build(name):
    """ Build all containers matching a name. """

    for config in [c for c in build_config if c['name'] == name]:
        _run_build(config)


def _run_build(config):
    """ Run the docker command to build a container, using its configuration
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
