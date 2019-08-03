import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-host-management',
    version='0.8',
    packages=find_packages(),
    include_package_data=True,
    description='host- management django app',
    long_description=README,
    url='https://www.example.com/',
    author='Jack',
    author_email='wangjievibeke@foxmail.com',
    install_requires=[
        'celery',
        'djangorestframework',
        'django-filter',
        'inflection',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django :: 1.11',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # Replace these appropriately if you are stuck on Python 2.
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
