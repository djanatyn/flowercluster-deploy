#!/usr/bin/env python

import string
from functools import wraps

import yaml
from fabric.api import task, prefix, hide, run, roles
from fabric.colors import green

from load_config import configuration
from tokens import save_token

vault_config = configuration['vault']
secrets = configuration['secrets']


def auth_vault(token=None):
    """ Authorize with vault API client. """

    if token is None:
        token = configuration['token']

    with hide('running', 'stdout', 'stderr'):
        run('vault auth ' + token)


def vault_task(f):
    """ Decorator for exporting VAULT environmental variables. """

    @wraps(f)
    def wrapper(*args, **kwargs):
        addr_prefix = prefix('export VAULT_ADDR=' + vault_config['VAULT_ADDR'])

        with addr_prefix:
            return f(*args, **kwargs)

    return task(wrapper)


@roles('flowercluster')
@vault_task
def unseal():
    """ Unseal the vault using keys specified by the user at deploy time. """

    for key in configuration['unseal_keys']:
        with hide('running', 'stdout', 'stderr'):
            run('vault unseal ' + key)


@roles('flowercluster')
@vault_task
def build_token():
    """ Generate and return a build token.

    Tokens are saved to $HOME/.flowercluster/tokens.yml.
    """
    auth_vault()

    token_args = ['vault token-create -format=yaml -policy=build-token']

    for arg, value in vault_config['build-token'].iteritems():
        token_args.append("-{0}={1}".format(arg, value))

    with hide('running', 'stdout'):
        token = yaml.load(run(string.join(token_args)))

    print(green('Build Token: ' + token['auth']['client_token']))
    save_token(token)
    return token['auth']['client_token']


@roles('flowercluster')
@vault_task
def init_secrets():
    """ Initialize secrets in $HOME/.flowercluster/secrets.yml. """

    auth_vault()

    for secret in secrets:
        cmd = ['vault write', secret['path']]

        for key, value in secret['data'].iteritems():
            cmd.append(key + '=' + value)

        run(string.join(cmd))
