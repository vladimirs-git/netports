"""Package setup"""

import pathlib

from setuptools import setup, find_packages  # type: ignore

import netports as packet

VERSION = "0.1.1"
PACKAGE = packet.__title__
ROOT = pathlib.Path(__file__).parent.resolve()
README = "README.rst"

if __name__ == "__main__":
    setup(
        name=PACKAGE,
        packages=[PACKAGE],
        package_data={PACKAGE: ["py.typed"]},
        version=VERSION,
        description=packet.__summary__,
        license=packet.__license__,
        long_description=open(README).read(),
        long_description_content_type="text/x-rst",
        author=packet.__author__,
        author_email=packet.__email__,
        url=packet.__url__,
        download_url=packet.__download_url__,
        keywords="interfaces, ports, tcp, network, telecommunication, cisco, ios",
        python_requires=">=3.8",
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Developers",
            "Intended Audience :: System Administrators",
            "Intended Audience :: Telecommunications Industry",
            "Topic :: System :: Networking",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3.8",
            "Natural Language :: English",
        ],
    )
