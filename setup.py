from distutils import core
import sys

from hockeyapp import __version__

requirements = ['requests']
tests_require = ['nose', 'mock', 'httmock']
if sys.version_info < (2, 7, 0):
    requirements.append('argparse')
    tests_require.append('unittest2')

console_scripts = ['hockeyapp-cli=hockeyapp.cli:main']

long_description = """Python client for the HockeyApp.net API"""
core.setup(name='hockeyapp',
           version=__version__,
           description="HockeyApp.net API",
           long_description=long_description,
           classifiers=[
            'Development Status :: 4 - Beta',
           ],
           author='Gavin M. Roy',
           author_email='gavinmroy@gmail.com',
           url='https://github.com/gmr/hockeyapp',
           packages=['hockeyapp'],
           entry_points=dict(console_scripts=console_scripts),
           zip_safe=True,
           install_requires=requirements,
           tests_require=tests_require)
