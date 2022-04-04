from typing import *

import requests as requests


def get(url: str, headers: Dict[str, str] = None, params: Dict[str, Any] = None) -> requests.Response:
    """
    :return: Json dictionary object of The schema.org for an Event in Reactome knowledgebase
    """

    if headers is None:
        headers = {}

    headers = {
        'accept': '*/*',
        **headers
    }

    try:
        response = requests.get(url=url, headers=headers, params=params)
        if response.status_code == 200:
            return response
        else:
            print(f'Status code returned a value of {response.status_code}')
    except ConnectionError as e:
        print(e)


def get_json(url: str, headers: Dict[str, str] = None, params: Dict[str, Any] = None) -> Any:
    """
    :return: Json dictionary object of The schema.org for an Event in Reactome knowledgebase
    """
    if headers is None:
        headers = {}
    headers = {
        'accept': 'application/json',
        **headers
    }
    r = get(url, headers, params)
    return r.json() if r else {}


def post(url: str, data: Any, headers: Dict[str, str] = None, params: Dict[str, Any] = None) -> requests.Response:
    """
    :return: Json dictionary object of The schema.org for an Event in Reactome knowledgebase
    """
    if headers is None:
        headers = {}

    headers = {
        'accept': '*/*',
        'content-type': 'text/plain',
        **headers
    }

    try:
        response = requests.post(url=url, headers=headers, params=params, data=data)
        if response.status_code == 200:
            return response
        else:
            print(f'Status code returned a value of {response.status_code}')
    except ConnectionError as e:
        print(e)


def post_json(url: str, data: Any, headers: Dict[str, str] = None, params: Dict[str, Any] = None) -> Any:
    """
    :return: Json dictionary object of The schema.org for an Event in Reactome knowledgebase
    """
    if headers is None:
        headers = {}

    headers = {
        'accept': 'application/json',
        'content-type': 'text/plain',
        **headers
    }

    r = post(url, data, headers, params)
    return r.json() if r else {}


def download(
        path: str, file_name: str, ext: str,
        url: str, headers: Dict[str, str] = None,
        params: Dict[str, Any] = None, chunk_size=None):
    if headers is None:
        headers = {}

    headers = {
        'accept': f'*/{ext}',
        **headers
    }

    if params is None:
        params = ()

    try:
        response = requests.get(url=url, headers=headers, params=params)
        if response.status_code == 200:
            with open(f'{path}{file_name}.{ext}', 'wb') as f:
                for chunk in response.iter_content(chunk_size):
                    f.write(chunk)
        else:
            print(f'Status code returned a value of {response.status_code}')
    except ConnectionError as e:
        print(e)
