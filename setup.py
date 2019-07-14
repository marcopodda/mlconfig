import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='mlconfig',
    version='0.1',
    author="Marco Podda",
    author_email="marco.podda@di.unipi.it",
    description="Config objects from ML projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/marcopodda/mlconfig",
    packages=setuptools.find_packages(),
    install_requires=[
       "pyyaml",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
 )