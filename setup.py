#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_namespace_packages


VERSION = '0.0.0'
LONGDESC = '''
AWS Organization configuration engine based on OrgCrawler
=========================================================
'''


setup(
    name='orgcrawler-task',
    version=VERSION,
    description='AWS Organization configuration engine based on OrgCrawler',
    long_description=LONGDESC,
    long_description_content_type='text/x-rst',
    url='https://github.com/ucopacme/orgcrawler-task',
    keywords='aws organizations boto3 orgcrawler',
    author='Ashley Gould - University of California Office of the President',
    author_email='agould@ucop.edu',
    license='GPLv3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    install_requires=[
        'botocore',
        'boto3',
        'orgcrawler',
        'PyYAML',
        'click',
        'cerberus',
    ],
    #packages=find_namespace_packages(include=['orgcrawler.*', 'orgcrawler.cli.*']),
    packages=find_namespace_packages(include=['orgcrawler.*']),
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'taskrunner=orgcrawler.cli.taskrunner:main',
        ],
    },
)
