import os
import sys
from setuptools import setup, find_packages

is_release = False
if "--release" in sys.argv:
    is_release = True
    sys.argv.remove("--release")

BASE = os.path.dirname(os.path.abspath(__file__))
README_PATH = os.path.join(BASE, "README.rst")

install_requires = [
    'aiohttp-transmute',
    'aiohttp_cors',
    'docopt',
    'jinja2',
]

setup(
    name="orbital-core",
    setup_requires=["vcver", "setuptools-parcels"],
      vcver={"is_release": is_release,
             "path": BASE},
    author="zillow-orbital",
    author_email="",
    description="common code for orbital's aiohttp services",
    license="",
    keywords="zillow",
    url="",
    packages=find_packages(),
    long_description=open(README_PATH).read(),
    classifiers=[
        "Topic :: Utilities",
    ],
    install_requires=install_requires,
    tests_require=[] + install_requires,
    entry_points={
        'console_scripts': [
            'generate_swagger_json=orbital_core.scripts.generate_swagger_json:main',
        ]
    },
    include_package_data=True,
    parcels={}
)
