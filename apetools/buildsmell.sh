#! /usr/bin/env bash

echo "Tagging this package"
pysmell . -x .be .hg apetools.egg-info documentation installables tests .tox
echo "Tagging the python2.7 standard library"
pysmell /usr/lib/python2.7/ -x site-packages test dist-packages -o PYSMELLTAGS.stdlib
echo "Tagging the third-party dependencies"
pysmell ../.tox/py27/lib/python2.7/site-packages/mock.py  ../.tox/py27/lib/python2.7/site-packages/nose ../.tox/py27/lib/python2.7/site-packages/numpy ../.tox/py27/lib/python2.7/site-packages/paramiko ../.tox/py27/lib/python2.7/site-packages/serial -o PYSMELLTAGS.dependencies



