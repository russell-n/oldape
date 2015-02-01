#!/usr/bin/env python

try:
    from setuptools import setup, find_packages
except ImportError:
    import distribute_setup
    distribute_setup.use_setuptools()
    from setuptools import setup, find_packages

from datetime import datetime

setup(name='apetools',
      version= datetime.today().strftime("0.0.3"),
      description="A program to run tests",
      author="russell",
      platforms=['linux'],
      url = '',
      author_email="rsnakamura@acm.org",
      license = "",
      install_requires = ['pudb', 'paramiko'],
      packages = find_packages(exclude=["__main__"]),
      include_package_data = True,
      package_data = {"apetools":["*.txt", "*.rst", "lexicographers/configfiles/*.ini"]},
      entry_points = """
	  [console_scripts]
          apetools=apetools.main:main
	  """
      )

# an example last line would be cpm= cpm.main: main

# If you want to require other packages add (to setup parameters):
# install_requires = [<package>],
#version=datetime.today().strftime("%Y.%m.%d"),
# if you have an egg somewhere other than PyPi that needs to be installed as a dependency, point to a page where you can download it:
# dependency_links = ["http://<url>"]
