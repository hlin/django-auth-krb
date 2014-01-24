#!/usr/bin/env python

from setuptools import setup, find_packages
from django_auth_krb import get_version

setup(
    name="django_auth_krb",
    version=get_version(),
    description="Django kerberos authentication backend",
    long_description=open('README.md').read(),
    url="https://github.com/hlin/django-auth-kerberos/",
    author="Hypo Lin",
    author_email="hlin.pub@me.com",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords=["django", "kerberos", "authentication", "auth"],
    packages=find_packages(exclude='tests'),
    include_package_data=True,
    install_requires=[
        'Django>=1.3',
        'kerberos==1.1.1',
    ],
    zip_safe=False,
)
