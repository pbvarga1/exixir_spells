from setuptools import setup


setup(
    name='spells_db',
    version='0.1.0',
    description='Database for storing magic spells',
    author='Perry Vargas',
    author_email='perrybvargas@gmail.com',
    packages=[
        'spells_db',
    ],
    package_dir={'spells_db': 'spells_db'},
    include_package_data=True,
    install_requires=[
        'SQLAlchemy==1.3.13',
    ],
    license="GNU",
    zip_safe=False,
    keywords='spells_db',
)
