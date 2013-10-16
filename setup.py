from distutils import core
import sys

from hockeyapp import __version__

requirements = ['requests']
tests_require = ['nose', 'mock', 'httmock']
if sys.version_info < (2, 7, 0):
    requirements.append('argparse')
    tests_require.append('unittest2')

console_scripts = ['hockeyapp-cli=hockeyapp.cli:main']

core.setup(name='hockeyapp',
           version=__version__,
           description='Python client for the HockeyApp.net API',
           long_description=open('README.rst').read(),
           author='Gavin M. Roy',
           author_email='gavinmroy@gmail.com',
           url='http://hockeyapp.readthedocs.org',
           packages=['hockeyapp'],
           entry_points=dict(console_scripts=console_scripts),
           zip_safe=True,
           package_data={'': ['LICENSE', 'README.md']},
           include_package_data=True,
           install_requires=requirements,
           tests_require=tests_require,
           test_suite='nose.collector',
           license=open('LICENSE').read(),
           classifiers=['Development Status :: 4 - Beta',
                        'Intended Audience :: Developers',
                        'License :: OSI Approved :: BSD License',
                        'Operating System :: OS Independent',
                        'Programming Language :: Python :: 2',
                        'Programming Language :: Python :: 2.6',
                        'Programming Language :: Python :: 2.7',
                        'Programming Language :: Python :: 3',
                        'Programming Language :: Python :: 3.2',
                        'Programming Language :: Python :: 3.3',
                        'Programming Language :: Python :: Implementation :: CPython',
                        'Programming Language :: Python :: Implementation :: PyPy',
                        'Topic :: Communications',
                        'Topic :: Internet',
                        'Topic :: Software Development :: Libraries'])
