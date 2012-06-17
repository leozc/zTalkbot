from setuptools import setup, find_packages
import os

setup(
    name='boboongae',
    version='1.0',
    author="Peter Parker",
    author_email="peter@web.org",
    description="Bobo on Google App Engine.",
    packages=find_packages(),
    package_dir={'': 'appeng'},
    include_package_data=True,
    install_requires=[
      'distribute',
    ],
)
