# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools.command.test import test as TestCommand
import sys


class Tox(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import tox
        errno = tox.cmdline(self.test_args)
        sys.exit(errno)


setup(
    name='hunk',
    version='0.1.0',
    description='Mock for JSON API server.',
    long_description=open('README.rst').read(),
    author='lanius',
    author_email='lanius@nirvake.org',
    url='https://github.com/lanius/hunk/',
    packages=['hunk'],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'hunk = hunk.server:main',
        ],
    },
    install_requires=['flask', 'requests'],
    license=open('LICENSE').read(),
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ),
    tests_require=['tox'],
    cmdclass = {'test': Tox}
)
