from setuptools import setup, find_packages

requires = [
    'tornado',
    'tornado-sqlalchemy',
    'psycopg2',
    'sqlalchemy',
]

setup(
    name='tornado_tutorial',
    version='0.0',
    description='Learning tornado',
    author='shubham',
    author_email='shubham.hapse@velotio.com',
    keywords='web tornado',
    packages=find_packages(),
    install_requires=requires,
    entry_points={
        'console_scripts': [
            'serve_app = todo:main',
        ],
    },
)