from setuptools import setup

name = "tehranse"
version = "1.0.1"
description = "TehranSE is a python library to access Tehran Stock Exchange data"
url = "https://github.com/SinaMobasheri/TehranSE"
author = "SinaMobasheri"
authoremail = "sinamobasheri@outlook.com"
packages = ["tehranse"]
platforms = ["platform independent"]
license = "GPL"
installrequires = ["requests", "beautifulsoup4"]
includepackagedata = True


longdescription = \
"""
# TehranSE
TehranSE is a python library to access Tehran Stock Exchange data

### Motivation
unfortunately, there is no suitable way to access financial information in Tehran Stock Exchange
TehranSE is trying to solve this problem

### Installation
`pip install tehranse`

### Getting Started
see homepage for more information

### License
[GNU General Public License Version 3.0](https://www.gnu.org/licenses/gpl-3.0.txt)
"""
longdescriptioncontenttype = "text/markdown"


setup(name=name, version=version, description=description, long_description=longdescription, long_description_content_type=longdescriptioncontenttype, url=url, author=author, author_email=authoremail, packages=packages, platforms=platforms, license=license, install_requires=installrequires, include_package_data=includepackagedata)