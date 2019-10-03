from setuptools import find_packages, setup

setup(name='viaa-chassis',
      version='0.0.2',
      url='https://github.com/viaacode/chassis.py',
      license='GPL',
      author='Rudolf',
      author_email='rudolf.degeijter@viaa.be',
      description='VIAA Chassis',
      packages=find_packages(exclude=['tests']),
      long_description=open('README.md', encoding="utf8").read(),
      zip_safe=False,
      install_requires=['structlog==19.1.0', 'pyyaml==5.1.2', 'python-json-logger==0.1.11']
)
