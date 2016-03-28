#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import find_packages, setup


setup(
    name='celery-gracefull-stop',
    version='0.0.1',
    description='Celery plugin thats adds ability to gracefull stop worker',
    author='Mikhail Antonov',
    author_email='atin65536@gmail.com',
    long_description=open('README.md').read(),
    url='https://github.com/MnogoByte/celery-gracefull-stop',
    packages=find_packages(),
    install_requires=["celery>=3.1"],
    keywords=['celery', 'stop', 'gracefull', 'reload'],
    classifiers=[
        "Framework :: Celery",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Development Status :: 1 - Alpha",
        "License :: OSI Approved :: BSD License",
    ],
    license="BSD"
)

