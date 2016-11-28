#!/usr/bin/env python

from fabric_gce_tools import update_roles_gce
from fabric.api import env

import vault
import instances
import containers

env.port = '2222'

update_roles_gce(use_cache=False)

__all__ = ['instances', 'vault', 'containers']
