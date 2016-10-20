#!/usr/bin/env python

import json
import yaml

from fabric.api import task, run, abort, cd, put, prefix, hide
from fabric_gce_tools import update_roles_gce

config = yaml.load(open('config.yml'))
config.update(yaml.load(open('secrets/secrets.yml')))


@task
def unseal_vault():
    """ Unseal the vault using keys specified by the user at deploy time. """

    with prefix('export VAULT_ADDR=' + config['url']):
        for key in config['unseal_keys']:
            with hide('running', 'stdout', 'stderr'):
                run('vault unseal ' + key)


@task
def registry_certs():
    """ Update registry certs. """

    output = run("docker volume inspect registry-certs", quiet=True)

    if output.failed:
        abort("couldn't find docker volume")

    path = json.loads(output)[0]['Mountpoint']
    with cd(path):
        put('secrets/registry-domain.crt', 'domain.crt', use_sudo=True)
        put('secrets/registry-domain.key', 'domain.key', use_sudo=True)


update_roles_gce()
