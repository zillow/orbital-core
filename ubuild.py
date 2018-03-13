import os
from setuptools import setup, find_packages

base = os.path.dirname(os.path.abspath(__file__))


def read(fname):
    '''Utility function to read the README file.'''
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

install_requires = [
    'arrow',
    'aiohttp-transmute',
    'aiohttp_cors',
    'docopt',
    'jinja2',
]

data_files = []

target = os.path.join(base, "zillow_aiohttp", "templates")
for root, dirs, files in os.walk(target):
    relative_root = root[len(target):]
    relative_root = relative_root.lstrip("/")
    for d in dirs:
        full_path = os.path.join(relative_root, "*")
        data_files.append(full_path)

route_templates = os.path.join(base, "zillow_aiohttp", "routes", "templates")
for root, dirs, files in os.walk(route_templates):
    relative_root = root[len(route_templates):]
    relative_root = relative_root.lstrip("/")
    for d in dirs:
        full_path = os.path.join(relative_root, "*")
        data_files.append(full_path)

setup(
    name="zillow-aiohttp",
    setup_requires=["vcver", "setuptools-parcels"],
    vcver={"path": base},
    author="mondev",
    author_email="mondev@zillowgroup.com",
    description="common code for orbital services",
    keywords="zillow",
    url="https://stash.atl.zillow.net/projects/LIBS/repos/egg.zillow-aiohttp/browse",
    packages=find_packages(),
    long_description=read('README.md'),
    classifiers=[
        "Topic :: Utilities",
    ],
    install_requires=install_requires,
    tests_require=[] + install_requires,
    entry_points={
        'console_scripts': [
            'install_zillow_aiohttp_templates=zillow_aiohttp.scripts.install_templates:main',
            'generate_swagger_json=zillow_aiohttp.scripts.generate_swagger_json:main',
        ]
    },
    package_data={"zillow_aiohttp": data_files},
    include_package_data=True,
)
