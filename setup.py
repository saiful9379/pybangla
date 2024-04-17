# import setuptools

# with open("README.md", "r", encoding = "utf-8") as fh:
#     long_description = fh.read()

# setuptools.setup(
#     name = "pybangla",
#     version = "0.0.1",
#     author = "saiful",
#     author_email = "saifulbrur79@gmail.com",
#     description = "format date to bangla date format and english digits convert to bangla digits",
#     long_description = long_description,
#     long_description_content_type = "text/markdown",
#     url = "package URL",
#     project_urls = {
#         "Bug Tracker": "package issues URL",
#     },
#     classifiers = [
#         "Programming Language :: Python :: 3",
#         "License :: OSI Approved :: MIT License",
#         "Operating System :: OS Independent",
#     ],
#     install_requires = {"DateTime"},
#     package_dir = {"": "src"},
#     packages = setuptools.find_packages(where="src"),
#     python_requires = ">=3.6"
# )

from setuptools import setup, find_packages

setup(
    name='example-package',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'Translator = src.main:Translator'
        ]
    },
    author='saiful',
    author_email='saifulbrur79@gmail.com',
    description='An example package',
    url='https://github.com/saiful9379/pybangla',
    license='MIT',
    install_requires=[
        # List of dependencies
    ]
)
