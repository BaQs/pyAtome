from __future__ import print_function
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import io
import codecs
import os
import sys

import pyatome 

here = os.path.abspath(os.path.dirname(__file__))

def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

# long_description = read('README.txt', 'CHANGES.txt')
long_description = read('README.md')

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)

setup(
    name='pyAtome',
    version=pyatome.__version__,
    url='http://github.com/baqs/pyAtome/',
    license='Apache Software License',
    author='Pierre Ourdouille',
    tests_require=['pytest'],
    install_requires=['requests',
                    'simplejson',
                    'fake_useragent',
                    'requests_mock'
                    ],
    cmdclass={'test': PyTest},
    author_email='baqs@users.github.com',
    description='Get your energy consumption from Atome Linky device',
    long_description=long_description,
    packages=['pyatome'],
    include_package_data=True,
    platforms='any',
    test_suite='pyAtome.test.test_pyatome',
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        ],
    entry_points={
        'console_scripts': [
            'pyatome = pyatome.__main__:main'
        ]
    },
    extras_require={
        'testing': ['pytest'],
    }
)
