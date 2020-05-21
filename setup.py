#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='photos2geojson',
    version='1.3',
    description="Makes geojson from EXIF data.",
    author="Visgean Skeloru",
    author_email='visgean@gmail.com',
    url='https://github.com/visgean/photos2geojson',
    packages=[
        'photos2geojson',
    ],
    package_dir={'photos2geojson': 'photos2geojson'},
    license="MIT",
    keywords='photos geojson exif',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    install_requires=[
        'requests',
        'exifread',
    ],
    entry_points={
        'console_scripts': [
            'photos2geojson = photos2geojson.main:main'
        ]
    },
    package_data={
        'photos2geojson': ['*.html']
    },
)