#!/usr/bin/env python

import string

from load_config import configuration
from fabric.api import task, local

instance_config = configuration['flowercluster-instance']


@task
def create_disks():
    """ Create disks for flowercluster instance. """

    args = [
        "gcloud compute disks create {}".format(instance_config['disk']),
        "--size={}".format(instance_config['disk-size']),
    ]

    local(string.join(args))


@task
def launch_instance():
    """ Launch flowercluster instance. """

    args = [
        'gcloud compute instances create flowercluster',
        '--metadata-from-file user-data=config/ignition.json',
        '--tags flowercluster',
        "--disk name={0},device-name={0}".format(instance_config['disk']),
        "--machine-type {}".format(instance_config['machine-type']),
        "--network {}".format(instance_config['network']),
        "--image {}".format(instance_config['image']),
    ]

    local(string.join(args))


@task
def delete_instance():
    """ Delete flowercluster instance. """

    return local('gcloud compute instances delete flowercluster')


@task
def recreate_instance():
    """ Delete and recreate flowercluster instance. """

    if delete_instance().succeeded:
        launch_instance()


@task
def update_metadata():
    """ Update the metadata with the configuration JSON. """

    args = [
        'gcloud compute instances add-metadata flowercluster',
        '--metadata-from-file user-data=config/ignition.json',
    ]

    return local(string.join(args))
