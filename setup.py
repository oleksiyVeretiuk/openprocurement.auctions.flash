from setuptools import setup, find_packages
import os

version = '1.2.2'

entry_points = {
    'openprocurement.auctions.core.plugins': [
        'auctions.flash = openprocurement.auctions.flash.includeme:includeme'
    ],
    'openprocurement.auctions.flash.plugins': [
        'flash.migration = openprocurement.auctions.flash.migration:migrate_data'
    ],
    'openprocurement.tests': [
        'auctions.flash = openprocurement.auctions.flash.tests.main:suite'
    ]
}
requires = [
    'setuptools',
    'openprocurement.auctions.core',
    'openprocurement.schemas.dgf',
    'schematics-flexible'
]
test_requires = requires + []

setup(
    name='openprocurement.auctions.flash',
    version=version,
    description="",
    long_description=open("README.rst").read() + "\n" + open(os.path.join("docs", "HISTORY.txt")).read(),
    # Get more strings from
    # http://pypi.python.org/pypi?:action=list_classifiers
    classifiers=[
      "Programming Language :: Python",
      ],
    keywords='',
    author='Quintagroup, Ltd.',
    author_email='info@quintagroup.com',
    license='Apache License 2.0',
    url='https://github.com/openprocurement/openprocurement.auctions.flash',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['openprocurement', 'openprocurement.auctions'],
    include_package_data=True,
    zip_safe=False,
    extras_require={'test': test_requires},
    install_requires=requires,
    test_require=test_requires,
    entry_points=entry_points,
    )
