from setuptools import setup, find_packages

requires = [
    'flask',
    'psycopg2'
]

setup(
    name='flask_pellet',
    version='0.0.1',
    description='Web app to search grain offers in Ukraine built with Flask',
    author='Kostiantyn Ivashchenko',
    author_email='konstantin.ivaschenko238@gmail.com',
    keywords='web flask postgresql',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires
)