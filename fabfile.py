#!/usr/bin/env python

import json
from getpass import getpass

from fabric.api import task, run
from fabric_gce_tools import update_roles_gce

api = 'http://localhost:8200/v1'


@task
def unseal_vault():
    """ Unseal the vault using keys specified by the user at deploy time. """

    url = api + '/sys/unseal'

    keys = [
        getpass(prompt='unseal key 1: '),
        getpass(prompt='unseal key 2: '),
        getpass(prompt='unseal key 3: '),
    ]

    print("---")

    for key in keys:
        data = json.dumps({'key': key})

        run("curl -X PUT -d '{0}' {1}".format(data, url))

update_roles_gce()
