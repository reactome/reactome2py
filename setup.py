from setuptools import setup, find_packages

__version__ = '0.0.1'

setup(
    name='reactome2py',
    version=__version__,
    description='Python client for Reactome content and analysis service API calls.',
    url='https://github.com/reactome/reactome2py',
    author='Nasim Sanati',
    author_email='nasim@plenary.org',
    license='Apache',
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
