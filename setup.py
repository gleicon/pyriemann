import sys, os, os.path, subprocess
from setuptools.command import easy_install
import pkg_resources as pkgrsrc

from setuptools import setup
from distutils import log
log.set_threshold(log.INFO)

setup(
        name            = "pyriemann",
        version         = "0.2",

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
        license         = "MIT",
        long_description = "pyriemann implements a Python client for Riemann, the network monitoring tool.\n" +
        "It requires protobuf-python, allowing you to send packets in either TCP or UDP.\n" +
        "Support for queries and events comes natively.\n",
    )

