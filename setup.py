#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = [
    "Click>=7.0",
]

test_requirements = []

setup(
    author="Megan Christina Davis",
    author_email="mdavis22@go.olemiss.edu",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="Various python utilities to make working with QFFs easier",
    entry_points={
        "console_scripts": [
            "testqffcli=qff_utils.cli:main",
            "testhello=qff_utils.hello.cli:main",
            "testqff_helper=qff_utils.qff_helper.cli:main",
            "testspec2latex=qff_utils.spec2latex.cli:main",
            "testxqpgen=qff_utils.xqpgen.cli:main"
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="qff_utils",
    name="qff_utils",
    packages=find_packages(include=["qff_utils", "qff_utils.*"]),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/MeganDavisChem/qff_utils",
    version="0.1.0",
    zip_safe=False,
)
