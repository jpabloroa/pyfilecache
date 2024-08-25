from setuptools import setup, find_packages

setup(
    name='pyfilecache',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'pandas==1.5.0',
        'pyarrow==11.0.0'
    ],
    test_suite='tests',
)
