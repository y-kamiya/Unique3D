from setuptools import find_packages, setup

setup(
    name="unique3d",
    version='"0.0.1"',  # the current version of your package
    packages=find_packages(),  # automatically discover all packages and subpackages
    install_requires=[
        # list of packages your project depends on
        # you can specify versions as well, e.g. 'numpy>=1.15.1'
    ],
    classifiers=[
        # classifiers help users find your project by categorizing it
        # for a list of valid classifiers, see https://pypi.org/classifiers/
        "Programming Language :: Python :: 3",
    ],
)
