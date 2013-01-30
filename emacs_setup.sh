#! /usr/bin/env sh

pip install -e hg+https://bitbucket.org/agr/rope#egg=rope
pip install -e hg+https://bitbucket.org/agr/ropemacs#egg=ropemacs
pip install -e hg+https://bitbucket.org/agr/ropemode#egg=ropemode
pip install -e git+https://github.com/pinard/Pymacs.git#egg=pymacs
pip install pysmell

cd .tox/py27/src/pymacs/
make
