#!/usr/bin/env python

import json
import yaml

from fabric.api import task, run, abort, cd, put
from fabric_gce_tools import update_roles_gce

config = yaml.load(open('config.yml'))
config.update(yaml.load(open('secrets/secrets.yml')))


@task
def unseal_vault():
    """ Unseal the vault using keys specified by the user at deploy time. """

    url = config['api'] + '/sys/unseal'

    for key in config['unseal_keys']:
        data = json.dumps({'key': key})

        run("curl -X PUT -d '{0}' {1}".format(data, url))


@task
def registry_certs():
    """ Update registry certs. """

    output = run("docker volume inspect registry-certs", quiet=True)

    if output.failed:
        abort("couldn't find docker volume")

    path = json.loads(output)[0]['Mountpoint']
    with cd(path):
        put('secrets/registry-domain.crt', 'domain.crt')
        put('secrets/registry-domain.key', 'domain.key')


update_roles_gce()
