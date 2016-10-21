#!/usr/bin/env python

import json
import yaml

from fabric.api import task, run, abort, cd, put, prefix, hide
from fabric_gce_tools import update_roles_gce

config = yaml.load(open('config.yml'))
config.update(yaml.load(open('secrets/secrets.yml')))


def vault(f):
    """ Decorator for export VAULT_ADDR. """

    @wraps(f)
    def wrapper(*args, **kwargs):
        with prefix('export VAULT_ADDR=' + config['url']):
            return f(*args, **kwargs)

    return wrapper


@task
@vault
def unseal_vault():
    """ Unseal the vault using keys specified by the user at deploy time. """

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


@task
def vault_policies():
    """ Update vault policies. """

    policies = yaml.load(open('policy.yml'))

    for name, policy in policies.iteritems():
        pass


update_roles_gce(use_cache=False)
