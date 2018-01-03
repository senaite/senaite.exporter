# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

version = '0.1.0'


setup(
    name='senaite.exporter',
    version=version,
    description="SENAITE EXPORTER",
    long_description="Changelog\n" +
                     "=========\n" +
                     open("docs/Changelog.rst").read() + "\n" +
                     "\n\n" +
                     "Authors and maintainers\n" +
                     "-----------------------\n\n" +
                     "- Pau Soliva (Naralabs) <psoliva@naralabs.com>",
    # Get more strings from
    # http://pypi.python.org/pypi?:action=list_classifiers
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Plone",
        "Framework :: Zope2",
    ],
    keywords=['bika', 'senaite', 'lists', 'exporter', 'lis', 'lims'],
    author='SENAITE Foundation',
    author_email='support@senaite.com',
    url='https://github.com/senaite/senaite.exporter',
    license='GPLv2',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['senaite'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'senaite.core',
        'setuptools',
        'senaite.api',
        'senaite.jsonapi',
        'requests',
        'plone.api',
    ],
    extras_require={
        'test': [
            'Products.PloneTestCase',
            'Products.SecureMailHost',
            'plone.app.testing',
            'robotsuite',
            'unittest2',
        ]
    },
    entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
)
