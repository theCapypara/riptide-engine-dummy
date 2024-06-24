__version__ = '0.8.0'

# README read-in
from os import path

from setuptools import setup, find_packages

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()
# END README read-in

setup(
    name='riptide-engine_dummy',
    version=__version__,
    packages=find_packages(),
    description='Tool to manage development environments for web applications using containers - Dummy Implementation',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://github.com/theCapypara/riptide-engine-dummy/',
    install_requires=[
        'riptide-lib >= 0.8.0, < 0.9',
        'docker >= 4.1'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    entry_points='''
        [riptide.engine]
        dummy=riptide_engine_dummy.engine:DummyEngine
    ''',
)
