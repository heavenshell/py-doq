import os

from setuptools import (
    find_packages,
    setup,
)

version = ''
with open('doq/__init__.py') as f:
    for line in f.readlines():
        if line.startswith('__version__'):
            version = line.split('=')[1].strip().replace("'", '')

rst_path = os.path.join(os.path.dirname(__file__), 'README.rst')
description = ''
with open(rst_path) as f:
    description = f.read()

setup(
    name='doq',
    version=version,
    author='Shinya Ohyanagi',
    author_email='sohyanagi@gmail.com',
    url='http://github.com/heavenshell/py-doq',
    description='Docstring generator',
    long_description=description,
    license='BSD',
    platforms='any',
    packages=find_packages(exclude=['tests']),
    package_dir={'': '.'},
    include_package_data=True,
    package_data={'doq': [
        'templates/google/*.txt',
        'templates/numpy/*.txt',
        'templates/sphinx/*.txt',
    ]},
    install_requires=['parso', 'jinja2'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Documentation',
        'Topic :: Software Development :: Documentation',
    ],
    entry_points="""
    [console_scripts]
    doq = doq.cli:main
    """,
    tests_require=['parameterized'],
    test_suite='tests',
)
