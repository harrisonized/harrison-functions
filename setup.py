from setuptools import setup, find_packages

with open('./README.md') as f:
    description = f.read()

setup(
    name='harrison-functions',
    description='Reusable functions',
    long_description=description,
    version='1.0',
    author='Harrison Wang',
    author_email='harrisonized@gmail.com',
    url='https://github.com/harrisonized/harrison_functions',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
)
