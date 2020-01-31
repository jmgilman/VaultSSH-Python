import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="vaultssh",
    version="1.0.0",
    description="CLI tool for signing SSH public keys using the Vault SSH endpoint",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/jmgilman/VaultSSH",
    author="Joshua Gilman",
    author_email="joshuagilman@gmail.com",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "certifi==2019.11.28",
        "chardet==3.0.4",
        "click==7.0",
        "hvac==0.9.6",
        "idna==2.8",
        "requests==2.22.0",
        "six==1.14.0",
        "urllib3==1.25.8",
    ],
    dependency_links=[],
    entry_points={"console_scripts": ["vaultssh=vaultssh.vaultssh:main"]},
)
