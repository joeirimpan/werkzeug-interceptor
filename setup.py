#!/usr/bin/env python

from setuptools import setup

setup(
    name="http-interceptor",
    version="0.1.3",
    description="Simple HTTP interceptor",
    author="Joe Paul",
    author_email="joeirimpan@gmail.com",
    packages=["interceptor"],
    download_url="https://github.com/joeirimpan/werkzeug-interceptor",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries"
    ],
    entry_points={
        'console_scripts': ['http_intercept=interceptor:execute']
    },
    install_requires=['werkzeug', 'colorama'],
)
