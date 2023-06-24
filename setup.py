import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION = "0.1.7"
PACKAGE_NAME = "Historic_Crypto"
AUTHOR = "Peter Linders"
AUTHOR_EMAIL = "plinders@gmail.com"
URL = "https://github.com/outlander-industries/Historic_Crypto"

LICENSE = "MIT License"
DESCRIPTION = (
    "An open source Python library for scraping Historical Cryptocurrency data."
)
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = ["numpy", "requests", "pandas", "tqdm"]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    author=AUTHOR,
    license=LICENSE,
    author_email=AUTHOR_EMAIL,
    url=URL,
    install_requires=INSTALL_REQUIRES,
    packages=find_packages(),
)
