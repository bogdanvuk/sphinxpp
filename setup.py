# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

long_desc = '''
This package contains the various Sphinx extensions.

.. add description here ..
'''

requires = ['Sphinx>=0.6']

setup(
    name='sphinxpp',
    version='0.1',
    url='https://github.com/bogdanvuk/rst',
    download_url = 'https://github.com/bogdanvuk/rst/tarball/0.0.1',
    license='BSD',
    author='Bogdan Vukobratovic',
    author_email='bogdan.vukobratovic@gmail.com',
    description='Various Sphinx extensions',
    long_description=long_desc,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Sphinx :: Extension',
        #'Framework :: Sphinx :: Theme',
        'Topic :: Documentation',
        'Topic :: Utilities',
    ],
    platforms='any',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
)
