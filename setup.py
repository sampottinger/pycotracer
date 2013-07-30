"""Standard setup script for pycotracer.

@author: A. Samuel Pottinger (Gleap LLC)
@license: GNU GPL v3
"""

from distutils.core import setup
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
    ]
)