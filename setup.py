from setuptools import setup, find_packages
from os import path
from glob import glob
from os.path import basename, splitext

here = path.abspath(path.dirname(__file__))
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="browse_dupfiles",  # Required
    # https://www.python.org/dev/peps/pep-0440/
    version="0.0.1",
    description="Browse duplicity backup logs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: System Administrators",
        "Topic :: System :: Systems Administration",
        "License :: Public Domain",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    keywords="backup user-interface",
    packages=find_packages(
        where="src", exclude=["contrib", "docs", "tests"]
    ),
    package_dir={'': 'src'},
    py_module=[splitext(basename(path))[0] for path in glob('src/*/*.py')],
    entry_points={  # Optional
        "console_scripts": ["browse_dupfiles=browse_dupfiles.cli:main"]
    },
)
