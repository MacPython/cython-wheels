####################################
Building and uploading Cython wheels
####################################

We automate wheel building using this custom github repository that builds on
the travis-ci OSX machines, travis-ci Linux machines, and the Appveyor VMs.

The travis-ci interface for the builds is
https://travis-ci.org/MacPython/cython-wheels

Appveyor interface at
https://ci.appveyor.com/project/matthew-brett/cython-wheels

The driving github repository is
https://github.com/MacPython/cython-wheels

Quickstart
==========

For building Cython version 0.26.2::

    python trigger_build.py 0.26.2

Then wait for the builds to finish.  Check:

* https://travis-ci.org/MacPython/cython-wheels
* https://ci.appveyor.com/project/matthew-brett/cython-wheels
* The Rackspace container where the wheels go:
  https://3f23b170c54c2533c070-1c8a9b3114517dc5fe17b7c3f8c63a43.ssl.cf2.rackcdn.com

When they are all done::

    pip install beautifulsoup4 twine
    python upload_wheels.py 0.26.2

How it works
============

The wheel-building repository:

* does a fresh build of any required C / C++ libraries;
* builds a Cython wheel, linking against these fresh builds;
* processes the wheel using delocate_ (OSX) or auditwheel_ ``repair``
  (Manylinux1_).  ``delocate`` and ``auditwheel`` copy the required dynamic
  libraries into the wheel and relinks the extension modules against the
  copied libraries;
* uploads the built wheels to a Rackspace container - see "Using the
  repository" above.  The containers were kindly donated by Rackspace to
  scikit-learn).

The resulting wheels are therefore self-contained and do not need any external
dynamic libraries apart from those provided as standard by OSX / Linux as
defined by the manylinux1 standard.

The ``.travis.yml`` file in this repository has a line containing the API key
for the Rackspace container encrypted with an RSA key that is unique to the
repository - see http://docs.travis-ci.com/user/encryption-keys.  This
encrypted key gives the travis build permission to upload to the Rackspace
containers we use to house the uploads.

Triggering a build
==================

You will likely want to edit the ``.travis.yml`` and ``appveyor.yml`` files to
specify the ``BUILD_COMMIT`` before triggering a build - see below.

You will need write permission to the github repository to trigger new builds
on the travis-ci interface.  Contact us on the mailing list if you need this.

You can trigger a build by:

* making a commit to the ``cython-wheels`` repository (e.g. with ``git commit
  --allow-empty``); or
* clicking on the circular arrow icon towards the top right of the travis-ci
  page, to rerun the previous build.

In general, it is better to trigger a build with a commit, because this makes
a new set of build products and logs, keeping the old ones for reference.
Keeping the old build logs helps us keep track of previous problems and
successful builds.

Which cython commit does the repository build?
===============================================

The ``cython-wheels`` repository will build the commit specified in the
``BUILD_COMMIT`` at the top of the ``.travis.yml`` and ``appveyor.yml`` files.
This can be any naming of a commit, including branch name, tag name or commit
hash.

Uploading the built wheels to PyPI
==================================

* release container visible at
  https://3f23b170c54c2533c070-1c8a9b3114517dc5fe17b7c3f8c63a43.ssl.cf2.rackcdn.com

Be careful, this link points to a container on a distributed content delivery
network.  It can take up to 15 minutes for the new wheel file to get updated
into the containers at the links above.

When the wheels are updated, you can download them to your machine manually,
and then upload them manually to PyPI, or by using twine_.  You can also use a
script for doing this, housed at :
https://github.com/MacPython/terryfy/blob/master/wheel-uploader

For the ``wheel-uploader`` script, you'll need twine and `beautiful soup 4
<bs4>`_.

You will typically have a directory on your machine where you store wheels,
called a `wheelhouse`.   The typical call for `wheel-uploader` would then
be something like::

    VERSION=0.24.2
    CDN_URL=https://3f23b170c54c2533c070-1c8a9b3114517dc5fe17b7c3f8c63a43.ssl.cf2.rackcdn.com
    wheel-uploader -u $CDN_URL -s -v -w ~/wheelhouse -t all Cython $VERSION

where:

* ``-u`` gives the URL from which to fetch the wheels, here the https address,
  for some extra security;
* ``-s`` causes twine to sign the wheels with your GPG key;
* ``-v`` means give verbose messages;
* ``-w ~/wheelhouse`` means download the wheels from to the local directory
  ``~/wheelhouse``.

``cython`` is the root name of the wheel(s) to download / upload, and
``0.24.2`` is the version to download / upload.

So, in this case, ``wheel-uploader`` will download all wheels starting with
``Cython-0.24.2-`` from http://wheels.scipy.org to ``~/wheelhouse``, then
upload them to PyPI.

Of course, you will need permissions to upload to PyPI, for this to work.

.. _manylinux1: https://www.python.org/dev/peps/pep-0513
.. _twine: https://pypi.python.org/pypi/twine
.. _bs4: https://pypi.python.org/pypi/beautifulsoup4
.. _delocate: https://pypi.python.org/pypi/delocate
.. _auditwheel: https://pypi.python.org/pypi/auditwheel
