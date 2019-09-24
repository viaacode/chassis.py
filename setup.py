from setuptools import find_packages, setup

setup(name='viaa',
      version='0.0.1',
      url='https://github.com/rudolfdg/viaa-chassis',
      license='MIT',
      author='Rudolf',
      author_email='rudolf.degeijter@viaa.be',
      description='VIAA Chassis',
      packages=find_packages(exclude=['tests']),
      long_description=open('README.md').read(),
      zip_safe=False,
      install_requires=['structlog==19.1.0']
)
