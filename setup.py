"""Standard setup script for pycotracer.

@author: A. Samuel Pottinger (Gleap LLC)
@license: GNU GPL v3
"""

import os

from distutils.core import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='pycotracer',
    version='0.1',
    packages=['pycotracer'],
    author='A. Samuel Pottinger',
    url='https://github.com/Samnsparky/pycotracer',
    description=('Unofficial Python micro-library providing programmatic '
        'access to Colorado Transparency in Contribution and Expenditure '
        'Reporting (TRACER) campaign finance data.'),
    license='GPLv3',
    keywords='tracer political financial contributions colorado',
    long_description=read('README'),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Legal Industry',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Sociology'
    ],
    download_url='https://github.com/Samnsparky/pycotracer/archive/master.zip'
)