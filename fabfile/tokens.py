#!/usr/bin/env python

import os
import yaml

token_path = [os.environ['HOME'], '.flowercluster', 'tokens.yml']
token_file = os.path.join(*token_path)


def save_token(token):
    """ Write the build token to disk.

    Args:
        token: the yaml emitted from the vault command line client
    """

    tokens = []
    if os.path.isfile(token_file):
        tokens = yaml.load(open(token_file))

    tokens.append(token)
    with open(token_file, 'w') as f:
        f.write(yaml.dump(tokens))


def load_token():
    """ Attempts to load a token from $HOME/.flowercluster/tokens.yml.

    Returns None if a valid token cannot be found.
    """

    if not os.path.exists(token_file):
        return None

    tokens = yaml.load(open(token_file))

    # return the last token we added
    return tokens[-1]['auth']['client_token']
