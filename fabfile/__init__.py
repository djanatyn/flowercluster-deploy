#!/usr/bin/env python

from fabric_gce_tools import update_roles_gce
from fabric.api import env, roles, task

import vault
import instances
import containers

env.port = '2222'

update_roles_gce(use_cache=False)


@roles('flowercluster')
@task
def deploy():
    """ Run a full deploy. """

    vault.unseal()
    vault.init_secrets()
    vault.build_token()

    containers.build_all()
    containers.start_all()


__all__ = ['instances', 'vault', 'containers', 'deploy']
