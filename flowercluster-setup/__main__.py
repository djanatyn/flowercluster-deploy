#!/usr/bin/env python

import argparse
import logging

from __init__ import compute

log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=log_format)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def parse_args():
    parser = argparse.ArgumentParser(
        description='initialize flowercluster on google compute engine')
    parser.add_argument('--vault-key', '-v', type=str, help='ansible vault key')

    return parser.parse_args()


def main():
    logger.info('starting.')

    args = parse_args()

    logger.info("vault key: {}".format(args.vault_key))


if __name__ == '__main__':
    main()
