import sys, os, os.path, subprocess
from setuptools.command import easy_install
import pkg_resources as pkgrsrc

from setuptools import setup
from distutils import log
log.set_threshold(log.INFO)

setup(
        name            = "pyriemann",
        version         = "0.1",

        packages        = ['riemann', 'riemann.pb'],
        zip_safe = False,
        install_requires = ['%s>=%s' % x for x in dict(
            protobuf    = "2.4.1",
        ).items()],

        # metadata for upload to PyPI
        author          = "Gleicon Moraes",
        author_email    = "gleicon@gmail.com",
        keywords        = "events reimann",
        description     = "python driver for riemann",
        url             = "https://github.com/gleicon/pyriemann",
    )

