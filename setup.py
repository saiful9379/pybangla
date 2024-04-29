
import codecs
from setuptools import setup, find_packages

setup(
    name='pybangla',
    version='0.0.1',
    packages=find_packages(),
    # entry_points={
    #     'console_scripts': [
    #         'pybangla = pybangla.main:Normalizer'
    #     ]
    # },
    author='saiful',
    author_email='saifulbrur79@gmail.com',
    description='date and number digits convert to bangla digits',

    long_description=codecs.open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    
    url='https://github.com/saiful9379/pybangla',
    license='MIT',
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "DateTime",
        "num2words"
    ],
    python_requires = ">=3.6"
)
