""" Upload wheels to PyPI

Usage:
    python upload_wheels.py COMMIT_NAME

    e.g.

    python upload_wheels.py 0.26.2

You should check first for the built wheels at:

https://3f23b170c54c2533c070-1c8a9b3114517dc5fe17b7c3f8c63a43.ssl.cf2.rackcdn.com

The wheels take up to 15 minutes to appear on the Rackspace CDN, after they
have been nominally uploaded.
"""

import os
import sys

from wheel_uploader import upload_wheels, get_parser


def main():
    try:
        pkg_version = sys.argv[1]
    except IndexError:
        raise RuntimeError('Specify version number to upload')
    if not os.path.exists('wheelhouse'):
        os.mkdir('wheelhouse')
    opts, args = get_parser().parse_args([])
    opts.wheel_dir = 'wheelhouse'
    opts.wheel_type = 'all'
    opts.sign = True
    opts.verbose = True
    upload_wheels('Cython', pkg_version, opts)


if __name__ == '__main__':
    main()
