
import codecs
from setuptools import setup, find_packages

setup(
    name='pybangla',
    version='2.0.4',
    packages=find_packages(),
    # entry_points={
    #     'console_scripts': [
    #         'pybangla = pybangla.main:Normalizer'
    #     ]
    # },
    author='saiful',
    author_email='saifulbrur79@gmail.com',
    description='pybangla is the bangla text normalizer tool, it use for text normalization like word to number and date formating purposes',

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
        "num2words",
        "python-Levenshtein",
        "fuzzywuzzy"
    ],
    python_requires = ">=3.6"
)
