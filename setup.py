# setup py
from distutils.core import setup

setup(name = 'returnServer',
    version = '0.1',
   # py_modules = ['meta'],
    packages = ['meta','scripts',
                'model'],
    scripts = ['server.py'],
)