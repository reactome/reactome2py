
### Reactome2py 
CI | Branch  | Build Status
 ---|---------|-------------
 Travis | master  | [![Build Status](https://travis-ci.com/reactome/reactome2py.svg?branch=master)](https://travis-ci.com/reactome/reactome2py)

[![reactome2py from PyPI](https://img.shields.io/pypi/v/reactome2py.svg)](https://pypi.python.org/pypi/reactome2py/)[![Supported Python Versions](https://img.shields.io/pypi/pyversions/reactome2py.svg)](https://pypi.python.org/pypi/reactome2py/) 
[![Anaconda-Server Badge](https://anaconda.org/reactome/reactome2py/badges/version.svg)](https://anaconda.org/reactome/reactome2py)

Python client for Reactome content and analysis services API calls. 

#### Installation 

- PyPI install using pip 
    ``` 
    (sudo) pip install reactome2py 
    ```

- from source    
    ``` shell script
    git clone repo
    cd reactome2py
    python setup.py install 
    ```
- Dockerfile 
   ```
   (sudo) docker build -t <tag-name>:latest
   (sudo) docker run -it --rm <tag-name>:latest
   ```

#### reactome2py Jupyter notebook use-case examples 

`demo` folder holds jupyter notebooks to show use-cases: 

#### API Documentation and json structures (Model section)

- Pathway Analysis Service: https://reactome.org/AnalysisService/#/
- Content Service: https://reactome.org/ContentService/#/

#### Reactome Pathway Browser Tour 

This video is useful in understanding how to fully use and interpret Reactome pathway browser features.  
https://www.youtube.com/watch?v=-skixrvI4nU

In depth user guides are available at: https://reactome.org/userguide
