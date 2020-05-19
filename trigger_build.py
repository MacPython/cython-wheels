""" Trigger a build for a given commit

Usage:
    python trigger_build.py COMMIT_NAME

    e.g.

    python trigger_build.py 0.26.2

You'll need git on your system path, and the repository ready to push up to
Github.
"""

import sys
import re
from subprocess import check_call


APPV_RE = re.compile('^(\s*)(BUILD_COMMIT:)(\s*)(.*)$')
APPV_SUB = r'\g<1>\g<2> {}'
TRAV_RE = re.compile('^(\s*)(- BUILD_COMMIT=)(.*)$')
TRAV_SUB = r'\g<1>\g<2>{}'


def main():
    commit_name = sys.argv[1]
    for fname, regexp, subst in (('appveyor.yml', APPV_RE, APPV_SUB),
                                 ('.travis.yml', TRAV_RE, TRAV_SUB)):
        subst = subst.format(commit_name)
        with open(fname, 'rt') as fobj:
            lines = fobj.readlines()
        with open(fname, 'wt') as fobj:
            for line in lines:
                line = regexp.sub(subst, line)
                fobj.write(line)
    check_call(['git', 'commit', '-a', '-m',
                'Trigger build for ' + commit_name])
    if '.' in commit_name:
        # assume it's a tag name and tag it for uploading
        check_call(['git', 'tag', '-a', '-m', commit_name, commit_name])
        check_call(['git', 'push', '--tags'])
    check_call(['git', 'push'])


if __name__ == '__main__':
    main()
