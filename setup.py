#!/usr/bin/env python

try:
    from setuptools import setup, find_packages
except ImportError:
    import distribute_setup
    distribute_setup.use_setuptools()
    from setuptools import setup, find_packages

from datetime import datetime

setup(name='tottest',
      version= datetime.today().strftime("%Y.%m.%d"),
      description="A program to run Throughput-Over-Time (TOT) tests",
      author="russell",
      platforms=['linux'],
      url = '',
      author_email="russellnakamura@us.allion.com",
      license = "",
      install_requires = ['pudb', 'paramiko', 'pexpect', 'pyserial', 'mock'],
      packages = find_packages(exclude=["__main__"]),
      include_package_data = True,
      package_data = {"":["*.txt", "*.rst", "*.ini"]},
      entry_points = """
	  [console_scripts]
          tot=tottest.main:main
	  """
      )

# an example last line would be cpm= cpm.main: main

# If you want to require other packages add (to setup parameters):
# install_requires = [<package>],
#version=datetime.today().strftime("%Y.%m.%d"),
# if you have an egg somewhere other than PyPi that needs to be installed as a dependency, point to a page where you can download it:
# dependency_links = ["http://<url>"]
