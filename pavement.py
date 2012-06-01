from datetime import datetime

from paver.easy import *
from paver.setuputils import setup
import paver.doctools



setup(name='throughputovertimetest',
      version=datetime.today().strftime("%Y.%m.%d"),
      packages=['tottest'],
      description="A program to run Throughput-Over-Time (TOT) tests",
      author="russell",
      platforms=['linux'],
      url = '',
      author_email="russellnakamura@us.allion.com",
      license = "",
      install_requires = ['pudb', 'paramiko', 'pexpect'],

      entry_points = """
	  [console_scripts]
          tot=tottest.main:main
	  """      )

options(
    sphinx=Bunch(builddir='build',
                 docroot="documentation",
                 sourcedir="source")
)

@task
@needs(['html', 'setuptools.command.bdist_egg'])
def bdist_egg():
    """Generate docs and source distributions."""
    return
