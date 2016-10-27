#!/usr/bin/env python

import os
import yaml


def load_config():
    """ load and return configuration dictionary """

    user_config = os.path.join(os.environ['HOME'], '.flowercluster')

    config_paths = [
        'config.yml',
        'secrets.yml'
    ]

    # add user paths
    config_paths += [os.path.join(user_config, path) for path in config_paths]

    config = {}
    for path in [path for path in config_paths if os.path.isfile(path)]:
        config.update(yaml.load(open(path)))

    return config
