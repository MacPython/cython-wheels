########################
Cython OSX wheel builder
########################

Repository to build Cython wheels.

By default, this repo builds the most recent tagged version of the Cython
repo. If you want to build a specific version, unset ``LATEST_TAG`` in the
``.travis.yml`` file, and update the Cython submodule to the version you
want to build.

To update to a particular version to build rather than the latest tag:

* Update Cython submodule with version you want to build:

    * cd Cython
    * git pull && git checkout DESIRED_TAG
    * cd ..
    * git add Cython
    * git commit

The wheels get uploaded to a `rackspace container
<http://a365fff413fe338398b6-1c8a9b3114517dc5fe17b7c3f8c63a43.r19.cf2.rackcdn.com>`_
pointed to by http://wheels.scikits-image.org.  The credentials for this container
are encrypted to this specific repo in the ``.travis.yml`` file, so the upload
won't work for you from another repo.  Either contact me to get set up, or
use another upload service such as github - see for example Jonathan Helmus'
`scikit-image wheels builder
<https://github.com/jjhelmus/scikit-image-ci-wheel-builder>`_

I got the rackspace credentials from Olivier Grisel - we might be able to share
this account across projects - again - please contact me or Olivier if you'd
like this to happen.
