#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = []

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author="Irem Nasir",
    author_email='iremnasir@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Python program that takes artist name as user input, trains a Multinomial Naive Bayes model and predicts the outcome artist of the lyrics given by the user.",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='Lyrics_Classifier',
    name='Lyrics_Classifier',
    packages=find_packages(include=['Lyrics_Classifier']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/iremnasir/Lyrics_Classifier',
    version='0.1.0',
    zip_safe=False,
)
