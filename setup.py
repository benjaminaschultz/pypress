#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='pypress',
      version='0.1',
      description='Convenvience wrappers for blogging from python scripts and the command line securely',
      author='Benjamin Schultz',
      author_email='benjamin.a.schultz@gmail.com',
      url='https://codeblue.umich.edu/git/glogpy',
      packages=['pypress'],
      license='BSD',
      test_suite='nose.collector',
      classifiers=[
          'Programming Language :: Python',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Environment :: Console',
          'Environment :: Web Environment',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Internet :: WWW/HTTP :: Site Management',
          'Topic :: Utilities',
          'Natural Language :: English',
      ],
      include_package_data=True,
)
