import os

from setuptools import setup

cwd = os.path.dirname(os.path.realpath(__file__))
file = os.path.join(cwd, 'requirements.txt')
with open(file) as f:
    dependencies = list(map(lambda x: x.replace("\n", ""), f.readlines()))

with open("README.md", 'r') as f:
    long_description = f.read()

setup(name='Historic_Crypto',
      version='0.2.0',
      description='Historical Crypto.',
      long_description=long_description,
      author='',
      url='https://github.com/ertosns/Historic_Crypto',
      install_requires=dependencies,
      packages=['Historic_Crypto'])
