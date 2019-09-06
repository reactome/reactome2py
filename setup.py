from setuptools import setup, find_packages
"""
import requests

reqRelease = requests.get("https://github.com/reactome/reactome2py/releases")
releaseVersion = reqRelease.json()[0]['tag_name']
__version__ = str(releaseVersion[1:len(releaseVersion)])
"""
__version__ = '1.0.0'

setup(
    name='reactome2py',
    version=__version__,
    description='Python client for Reactome content and analysis service API calls.',
    url='https://github.com/reactome/reactome2py',
    author='Nasim Sanati',
    author_email='nasim@plenary.org',
    license='MIT',
    packages=find_packages(),
    entry_points={
        'console_scripts': ['reactome2py = reactome2py.__main__:main']
    },
    install_requires=[
        'requests'
    ],
    extras_require={
        'pandas': ["pandas==0.24.2"],
        'json': ["json5==0.8.4"],
    },
    tests_require=['pytest'])
