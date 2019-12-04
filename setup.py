from setuptools import setup, find_packages
import json

__version__ = '0.0.4'

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='reactome2py',
    version=__version__,
    description='Python client for Reactome content and analysis service API calls.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/reactome/reactome2py',
    author='Nasim Sanati',
    author_email='nasim@plenary.org',
    license='Apache',
  
    packages=find_packages(),
    entry_points={
        'console_scripts': ['reactome2py = reactome2py.__main__:main']
    },
    install_requires=[
        'requests',
    ],
    extras_require={
        'pandas': ['pandas==0.24.2'],
        'json': ['json5==0.8.4'],
    },
    tests_require=['pytest'],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: Apache Software License',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Software Development :: Libraries',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Bio-Informatics'
    ],
    platforms=['any'],
    python_requires='>=3.6',
)
