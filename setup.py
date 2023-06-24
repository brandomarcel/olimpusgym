from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in olimpusgym/__init__.py
from olimpusgym import __version__ as version

setup(
	name="olimpusgym",
	version=version,
	description="Sistema para la gestion de gimnasios",
	author="Brando Cevallos",
	author_email="brandocevallos@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
