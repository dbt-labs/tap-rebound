#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='tap-rebound',
      version='0.0.1',
      description='Singer.io tap for extracting data from the Rebound API',
      author='Fishtown Analytics',
      url='http://fishtownanalytics.com',
      classifiers=['Programming Language :: Python :: 3 :: Only'],
      py_modules=['tap_rebound'],
      install_requires=[
          'tap-framework==0.0.4',
      ],
      entry_points='''
          [console_scripts]
          tap-rebound=tap_rebound:main
      ''',
      packages=find_packages(),
      package_data={
          'tap_rebound': [
              'schemas/*.json'
          ]
      })
