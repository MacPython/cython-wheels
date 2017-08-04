#!/usr/bin/env python
""" Adds a build number to passed wheel filenames

Usage:

    python add_build_no.py <build_tag> <whl_fname> [<whl_fname> ...]

E.g.

    python add_build_no.py 1 h5py-2.6.0-*whl

This will give you output like so::

    Copying h5py-2.6.0-cp27-cp27m-manylinux1_i686.whl to h5py-2.6.0-1-cp27-cp27m-manylinux1_i686.whl
    Copying h5py-2.6.0-cp27-cp27m-manylinux1_x86_64.whl to h5py-2.6.0-1-cp27-cp27m-manylinux1_x86_64.whl
    Copying h5py-2.6.0-cp27-cp27mu-manylinux1_i686.whl to h5py-2.6.0-1-cp27-cp27mu-manylinux1_i686.whl
    Copying h5py-2.6.0-cp27-cp27mu-manylinux1_x86_64.whl to h5py-2.6.0-1-cp27-cp27mu-manylinux1_x86_64.whl
    Copying h5py-2.6.0-cp34-cp34m-manylinux1_i686.whl to h5py-2.6.0-1-cp34-cp34m-manylinux1_i686.whl
    Copying h5py-2.6.0-cp34-cp34m-manylinux1_x86_64.whl to h5py-2.6.0-1-cp34-cp34m-manylinux1_x86_64.whl
    Copying h5py-2.6.0-cp35-cp35m-manylinux1_i686.whl to h5py-2.6.0-1-cp35-cp35m-manylinux1_i686.whl
    Copying h5py-2.6.0-cp35-cp35m-manylinux1_x86_64.whl to h5py-2.6.0-1-cp35-cp35m-manylinux1_x86_64.whl
"""
from __future__ import print_function

import os
from os.path import split as psplit, join as pjoin
from shutil import copyfile
import argparse

from wheel.install import WheelFile

def make_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--build-suffix',
                        type=str,
                        default='-',
                        help='Suffix for build number')
    parser.add_argument('-r', '--rename',
                        action='store_true',
                        help='If set, remove original wheel')
    parser.add_argument('build_tag', help="Build tag")
    parser.add_argument('files', nargs="*", help="Input files")
    return parser


def main():
    args = make_parser().parse_args()
    for wheel_fname in args.files:
        path, fname = psplit(wheel_fname)
        wf = WheelFile(fname)
        parsed = wf.parsed_filename.groupdict()
        parsed['build'] = args.build_tag
        parsed['build_suffix'] = args.build_suffix
        out_fname = ('{name}-{ver}{build_suffix}{build}-{pyver}-{abi}-{plat}'
                     '.whl'.format(**parsed))
        out_path = pjoin(path, out_fname)
        print('{} {} to {}'.format(
            'Renaming' if args.rename else 'Copying', wheel_fname, out_path))
        copyfile(wheel_fname, out_path)
        if args.rename:
            os.unlink(wheel_fname)


if __name__ == '__main__':
    main()
