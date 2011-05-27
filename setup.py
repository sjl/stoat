from setuptools import setup

install_requires = ['django-treebeard', 'django-templatetag-sugar']

description = 'A sleek, lightweight, pluggable CMS app for Django.'
long_description = description

setup(
    name='stoat',
    version='0.4.0',
    install_requires=install_requires,
    description=description,
    long_description=long_description,
    author='Steve Losh',
    author_email='steve@stevelosh.com',
    url='http://bitbucket.org/sjl/stoat/',
    packages=['stoat'],
)
