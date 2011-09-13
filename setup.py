"""
setup.py

"""
__author__ = 'Gavin M. Roy'
__email__ = 'gmr@myyearbook.com'
__since__ = '2011-09-13'

from hockeyapp import __version__
from setuptools import setup

long_description = """Python client for the HockeyApp.net API"""
setup(name='hockeyapp',
      version=__version__,
      description="HockeyApp.net API",
      long_description=long_description,
      classifiers=[
        'Development Status :: 4 - Beta',
      ],
      author='Gavin M. Roy',
      author_email='gmr@myyearbook.com',
      url='http://github.com/gmr/hockeyapp',
      packages=['hockeyapp'],
      entry_points=dict(console_scripts=['hockeyapp-cli=hockeyapp.cli:main']),
      zip_safe=True)
