import io

from setuptools import setup

PACKAGE_ROOT = 'gtfs_realtime_translators'

with open('README.md') as readme_file:
    readme = readme_file.read()

about = dict()
with io.open(f'{PACKAGE_ROOT}/__version__.py', 'r', encoding='utf-8') as f:
    exec(f.read(), about)

requirements = [
    'gtfs-realtime-bindings==1.0.0',
    'pendulum==3.0.0',
    'xmltodict==0.13.0',
]

setup(
    name="gtfs-realtime-translators",
    version=about['__version__'],
    description='Translating custom arrivals formats to GTFS-realtime.',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Tyler Green',
    author_email='tyler.green@intersection.com',
    url='https://github.com/Intersection/gtfs-realtime-translators',
    packages=[
        f'{PACKAGE_ROOT}.translators',
        f'{PACKAGE_ROOT}.factories',
        f'{PACKAGE_ROOT}.registry',
        f'{PACKAGE_ROOT}.bindings',
        f'{PACKAGE_ROOT}.validators',
    ],
    license=about['__license__'],
    install_requires=requirements,
)
