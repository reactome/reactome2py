"""
utility functions for Reactome data-fetch, mappings, and overlay networks
"""
from requests.exceptions import ConnectionError
import requests
import io
import tarfile
import zipfile


def ehld_stids():
    """

    :return:
    """

    url = "https://reactome.org/download/current/ehld/svgsummary.txt"

    try:
        response = requests.get(url=url)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        content_list = response.text.splitlines()
        st_ids = [stId for stId in content_list if 'R-' in stId]
        return st_ids
    else:
        print('Status code returned a value of %s' % response.status_code)


def sbgn_stids():
    """

    :return:
    """

    url = "https://reactome.org/download/current/homo_sapiens.sbgn.tar.gz"

    try:
        response = requests.get(url=url)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        tar_file = tarfile.open(fileobj=io.BytesIO(response.content))
        file_names = tarfile.getnames()
        # helper function
        # ehlds = ehld_stids()
        # sbgns = [f.replace('.sbgn', '') for f in file_names]
        # set(sbgns) - set(ehlds)
    else:
        print('Status code returned a value of %s' % response.status_code)


def _yield_zip(response):
    """

    :param response:
    :return:
    """

    with zipfile.ZipFile(io.BytesIO(response.content)) as the_zip:
        for zip_info in the_zip.infolist():
            with the_zip.open(zip_info) as the_file:
                yield the_file.readlines()


def _read_ziplines(response):
    """

    :param response:
    :return:
    """

    return [c.split('\t') for c in [c.decode('utf8') for c in list(_yield_zip(response))[0]]]


def gene_mappings():
    """

    :return:
    """

    url = "https://reactome.org/download/current/ReactomePathways.gmt.zip"

    try:
        response = requests.get(url=url)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return _read_ziplines(response)
    else:
        print('Status code returned a value of %s' % response.status_code)
