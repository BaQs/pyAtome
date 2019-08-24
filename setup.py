import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='pyAtome',
    version="0.0.13",
    license='Apache Software License',
    author='Pierre Ourdouille',
    author_email='baqs@users.github.com',
    description='Get your energy consumption from Atome Linky device',
    long_description=long_description,
    url='http://github.com/baqs/pyAtome/',
    packages=setuptools.find_packages(include=['pyatome']),
    setup_requires=[
        'requests',
        'setuptools'
    ],
    install_requires=[
        'requests',
        'fake_useragent',
        'simplejson'
    ],
    entry_points={
    'console_scripts': [
        'pyatome = pyatome.__main__:main'
    ]
    }
)
