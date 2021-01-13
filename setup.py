import os
import codecs
from setuptools import setup


VERSION = '1.3.0'


def read(*parts):
    filename = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(filename, encoding='utf-8') as fp:
        return fp.read()


setup(
    name='pytest-isort',
    description='py.test plugin to check import ordering using isort',
    long_description=read('README.rst'),
    version=VERSION,
    license='BSD',
    author='Moccu GmbH & Co. KG',
    author_email='info@moccu.com',
    url='http://github.com/moccu/pytest-isort/',
    py_modules=['pytest_isort'],
    entry_points={'pytest11': ['isort = pytest_isort']},
    test_suite='.',
    install_requires=['isort>=4.0'],
    extras_require={'tests': ['mock']},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
