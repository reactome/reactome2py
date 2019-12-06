"""
Pathway Analysis Service
Provides pathway over-representation and expression analysis as well as species comparison tool \n
API calls are avaialble @ https://reactome.org/AnalysisService/#/ \n
Data model key classes for id query are available @ https://reactome.org/documentation/data-model
"""
from __future__ import print_function
from __future__ import unicode_literals
from requests.exceptions import ConnectionError
import csv
import requests
import pandas


NumberTypes = (int, float, complex)


def identifier(id='EGFR', interactors=False, page_size='1', page='1', species='Homo Sapiens', sort_by='ENTITIES_FDR',
               order='ASC', resource='TOTAL', p_value='1', include_disease=True, min_entities=None, max_entities=None,
               projection=False):
    """
    Given a protein, gene, or small molecule identifier symbol conducts analysis of the identifier over different species
    and pathways in reactome database.

    :param id: A protein, gene or small molecule identifier symbol id ex. EGFR
    :param interactors: Boolean value if set to false, your query will consider only manually curated Reactome pathways
        with known biological significance. if true, your query will consider Reactome pathways that have been expanded by
        including all available protein-protein interactors from the IntAct database
    :param page_size: Page size
    :param page: Number of pages
    :param species: List of species to filter the result (accepts taxonomy ids, species names and reactome dbId)
    :param sort_by: How to sort the result. Available filters TOTAL_ENTITIES, TOTAL_REACTIONS, TOTAL_INTERACTIONS,
        FOUND_ENTITIES, FOUND_INTERACTIONS, FOUND_REACTIONS, ENTITIES_RATIO, ENTITIES_PVALUE, ENTITIES_FDR, REACTIONS_RATIO
    :param order: Order ASC or DESC
    :param resource: The resource to sort TOTAL, UNIPORT, ENSEMBLE, CHEMBI, IUPHAR, MIRBASE, NCBI_PROTEIN, EMBL, COMPOUND, PUBCEM_COMPOUND
    :param p_value: Defines the pValue threshold. Only hit pathway with pValue equals or below the threshold will be returned
    :param include_disease: Set to ‘false’ to exclude the disease pathways from the result (it does not alter the statistics)
    :param projection: If true, projects the identifiers to human and only shows the result in this species
    :param max_entities: Maximum number of contained entities per pathway (takes into account the resource)
    :param min_entities: Minimum number of contained entities per pathway (takes into account the resource)
    :return: Json dictionary object
    """

    if isinstance(page_size, NumberTypes):
        page_size = str(page_size)

    if isinstance(page, NumberTypes):
        page = str(page)

    if isinstance(p_value, NumberTypes):
        p_value = str(p_value)

    if isinstance(min_entities, NumberTypes):
        min_entities = str(min_entities)

    if isinstance(max_entities, NumberTypes):
        max_entities = str(max_entities)

    if interactors:
        interactors = 'true'
    else:
        interactors = 'false'

    if include_disease:
        include_disease = 'true'
    else:
        include_disease = 'false'

    headers = {
        'accept': 'application/json',
    }

    params = (
        ('interactors', interactors),
        ('pageSize', page_size),
        ('page', page),
        ('sortBy', sort_by),
        ('order', order),
        ('species', species),
        ('resource', resource),
        ('pValue', p_value),
        ('includeDisease', include_disease),
        ('min', min_entities),
        ('max', max_entities),
    )

    url = 'https://reactome.org/AnalysisService/identifier/'

    if projection:
        url_gene = "".join([url, id, "/projection"])
    else:
        url_gene = "".join([url, id])

    try:
        response = requests.get(url=url_gene, headers=headers, params=params)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print('Status code returned a value of %s' % response.status_code)


def identifiers(ids='EGF,EGFR', interactors=False, page_size='1', page='1', species='Homo Sapiens',
                sort_by='ENTITIES_FDR', order='ASC', resource='TOTAL', p_value='1', include_disease=True,
                min_entities=None, max_entities=None, projection=False):
    """
    Given a list of protein, gene, or small molecule identifiers conducts reactome pathway enrichment analysis.

    :param ids: comma seperated list of proteins, genes or small molecules identifiers symbol in string format ex. 'EGF,EGFR'
    :param interactors: boolean value indicating include interations
    :param page_size: page size
    :param page: number of pages
    :param species: list of species to filter the result (accepts taxonomy ids, species names and dbId)
    :param sort_by: how to sort the result. Available filters: TOTAL_ENTITIES, TOTAL_REACTIONS, TOTAL_INTERACTIONS,
        FOUND_ENTITIES, FOUND_INTERACTIONS, FOUND_REACTIONS, ENTITIES_RATIO, ENTITIES_PVALUE, ENTITIES_FDR, REACTIONS_RATIO
    :param order: order ASC or DESC
    :param resource: the resource to sort TOTAL, UNIPORT, ENSEMBLE, CHEMBI, IUPHAR, MIRBASE, NCBI_PROTEIN, EMBL, COMPOUND, PUBCEM_COMPOUND
    :param p_value: defines the pValue threshold. Only hit pathway with pValue equals or below the threshold will be returned
    :param include_disease: set to ‘false’ to exclude the disease pathways from the result (it does not alter the statistics)
    :param projection: if true, projects the identifiers to human and only shows the result in this species
    :param max_entities: maximum number of contained entities per pathway (takes into account the resource)
    :param min_entities: minimum number of contained entities per pathway (takes into account the resource)
    :return: Json dictionary object
    """

    if isinstance(page_size, NumberTypes):
        page_size = str(page_size)

    if isinstance(page, NumberTypes):
        page = str(page)

    if isinstance(p_value, NumberTypes):
        p_value = str(p_value)

    if isinstance(min_entities, NumberTypes):
        min_entities = str(min_entities)

    if isinstance(max_entities, NumberTypes):
        max_entities = str(max_entities)

    if interactors:
        interactors = 'true'
    else:
        interactors = 'false'

    if include_disease:
        include_disease = 'true'
    else:
        include_disease = 'false'

    headers = {
        'accept': 'application/json',
        'content-type': 'text/plain',
    }

    params = (
        ('interactors', interactors),
        ('pageSize', page_size),
        ('page', page),
        ('sortBy', sort_by),
        ('order', order),
        ('species',  species),
        ('resource', resource),
        ('pValue', p_value),
        ('includeDisease', include_disease),
        ('min', min_entities),
        ('max', max_entities),
    )

    if projection:
        url = 'https://reactome.org/AnalysisService/identifiers/projection'
    else:
        url = 'https://reactome.org/AnalysisService/identifiers/'

    data = ids

    try:
        response = requests.post(url=url, headers=headers, params=params, data=data)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print('Status code returned a value of %s' % response.status_code)


def identifiers_form(path, interactors=False, page_size='1', page='1', species='Homo Sapiens', sort_by='ENTITIES_FDR',
                     order='ASC', resource='TOTAL', p_value='1', include_disease=True, min_entities=None, max_entities=None,
                     projection=False):
    """
    Given a file path with a list of identifiers conducts reactome pathway enrichment analysis

    :param path: absolute path to the the txt file with identifier symbols to be analysed - refer to https://reactome.org/dev/analysis for format.
    :param interactors: boolean value if set to false, your query will consider only manually curated Reactome
        pathways with known biological significance. if true, your query will consider Reactome pathways that
        have been expanded by including all available protein-protein interactors from the IntAct database.
    :param page_size: page size
    :param page: number of pages
    :param species: list of species to filter the result (accepts taxonomy ids, species names and dbId)
    :param sort_by: how to sort the result. Available filters: TOTAL_ENTITIES, TOTAL_REACTIONS, TOTAL_INTERACTIONS, FOUND_ENTITIES,
        FOUND_INTERACTIONS, FOUND_REACTIONS, ENTITIES_RATIO, ENTITIES_PVALUE, ENTITIES_FDR, REACTIONS_RATIO
    :param order: order ASC or DESC
    :param resource: the resource to sort TOTAL, UNIPORT, ENSEMBLE, CHEMBI, IUPHAR, MIRBASE, NCBI_PROTEIN, EMBL, COMPOUND, PUBCEM_COMPOUND
    :param p_value: defines the pValue threshold. Only hit pathway with pValue equals or below the threshold will be returned
    :param include_disease: set to ‘false’ to exclude the disease pathways from the result (it does not alter the statistics)
    :param projection: if true, projects the identifiers to human and only shows the result in this species
    :param max_entities: maximum number of contained entities per pathway (takes into account the resource)
    :param min_entities: minimum number of contained entities per pathway (takes into account the resource)
    :return:
    """

    if isinstance(page_size, NumberTypes):
        page_size = str(page_size)

    if isinstance(page, NumberTypes):
        page = str(page)

    if isinstance(p_value, NumberTypes):
        p_value = str(p_value)

    if isinstance(min_entities, NumberTypes):
        min_entities = str(min_entities)

    if isinstance(max_entities, NumberTypes):
        max_entities = str(max_entities)

    if interactors:
        interactors = 'true'
    else:
        interactors = 'false'

    if include_disease:
        include_disease = 'true'
    else:
        include_disease = 'false'

    headers = {
        'Content-Type': 'text/plain',
    }

    params = (
        ('interactors', interactors),
        ('pageSize', page_size),
        ('page', page),
        ('sortBy', sort_by),
        ('order', order),
        ('species',  species),
        ('resource', resource),
        ('pValue', p_value),
        ('includeDisease', include_disease),
        ('min', min_entities),
        ('max', max_entities),
    )

    if projection:
        url = 'https://reactome.org/AnalysisService/identifiers/form/projection'
    else:
        url = 'https://reactome.org/AnalysisService/identifiers/form/'

    data = open(path, 'rb').read()

    try:
        response = requests.post(url=url, headers=headers, params=params, data=data)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print('Status code returned a value of %s' % response.status_code)


def identifiers_url(external_url, interactors=False, page_size='1', page='1', species='Homo Sapiens', sort_by='ENTITIES_FDR',
                    order='ASC', resource='TOTAL', p_value='1', include_disease=True, min_entities=None, max_entities=None,
                    projection=False):
    """
    Given a url with a list of identifiers conducts reactome pathway enrichment analysis

    :param external_url: Url containing identifiers id symbols
    :param interactors: Boolean value if set to false, your query will consider only manually curated Reactome pathways
        with known biological significance. if true, your query will consider Reactome pathways that have been expanded by
        including all available protein-protein interactors from the IntAct database.
    :param page_size: Page size
    :param page: Number of pages
    :param species: List of species to filter the result (accepts taxonomy ids, species names and dbId)
    :param sort_by: How to sort the result. Available filters: TOTAL_ENTITIES, TOTAL_REACTIONS, TOTAL_INTERACTIONS, FOUND_ENTITIES,
        FOUND_INTERACTIONS, FOUND_REACTIONS, ENTITIES_RATIO, ENTITIES_PVALUE, ENTITIES_FDR, REACTIONS_RATIO
    :param order: Order ASC or DESC
    :param resource: The resource to sort TOTAL, UNIPORT, ENSEMBLE, CHEMBI, IUPHAR, MIRBASE, NCBI_PROTEIN, EMBL, COMPOUND, PUBCEM_COMPOUND
    :param p_value: Defines the pValue threshold. Only hit pathway with pValue equals or below the threshold will be returned
    :param include_disease: Set to ‘false’ to exclude the disease pathways from the result (it does not alter the statistics)
    :param projection: If true, projects the identifiers to human and only shows the result in this species
    :param max_entities: Maximum number of contained entities per pathway (takes into account the resource)
    :param min_entities: Minimum number of contained entities per pathway (takes into account the resource)
    :return:
    """

    if isinstance(page_size, NumberTypes):
        page_size = str(page_size)

    if isinstance(page, NumberTypes):
        page = str(page)

    if isinstance(p_value, NumberTypes):
        p_value = str(p_value)

    if isinstance(min_entities, NumberTypes):
        min_entities = str(min_entities)

    if isinstance(max_entities, NumberTypes):
        max_entities = str(max_entities)

    if interactors:
        interactors = 'true'
    else:
        interactors = 'false'

    if include_disease:
        include_disease = 'true'
    else:
        include_disease = 'false'

    headers = {
        'Content-Type': 'text/plain',
    }

    params = (
        ('interactors', interactors),
        ('pageSize', page_size),
        ('page', page),
        ('sortBy', sort_by),
        ('order', order),
        ('species',  species),
        ('resource', resource),
        ('pValue', p_value),
        ('includeDisease', include_disease),
        ('min', min_entities),
        ('max', max_entities),
    )

    if projection:
        url = 'https://reactome.org/AnalysisService/identifiers/url/projection'
    else:
        url = 'https://reactome.org/AnalysisService/identifiers/url/'

    data = external_url

    try:
        response = requests.post(url=url, headers=headers, params=params, data=data)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print('Status code returned a value of %s' % response.status_code)


def result2json(token, path='', file='result.json', save=False, gzip=False, chunk_size=128):
    """
    View of analysis result in json format

    :param token: The token associated with the data result - analysis Web-Service is token based, so for every analysis
        request a TOKEN is associated to the result
    :param path: Absolute path to save the file containing analysis results to
    :param file: File name to save the analysis results to
    :param save: Boolean value if true - saves result as json file. default is set to false.
    :param gzip: Boolean value if true - saves result as gzipped json file. default is set to false.
    :param chunk_size: Python generator iter_content() chunk size - default set to 128
    :return: File or json object containing data on pathway, entities, statistics, etc. found in analysis overlap
    """

    headers = {
        'accept': 'application/json',
    }

    if save or gzip:
        url = 'https://reactome.org/AnalysisService/download/%s/result.json.gzip' % token
    else:
        url = 'https://reactome.org/AnalysisService/download/%s/result.json' % token

    try:
        response = requests.get(url=url, headers=headers)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        if save or gzip:
            with open("".join([path, file]), 'wb') as f:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    f.write(chunk)
        else:
            return response.json()
    else:
        print('Status code returned a value of %s' % response.status_code)


def pathway2df(token, path='', resource='TOTAL', file='result.csv', save=False, chunk_size=128):
    """
    Create a Data frame of the analysis result for all the pathway hits - save to csv file (comma separated)

    :param token: The token associated with the data result - analysis Web-Service is token based, so for every analysis
        request a TOKEN is associated to the result
    :param path: Absolute path to save the file containing analysis results to
    :param resource: The resource to sort TOTAL, UNIPORT, ENSEMBLE, CHEMBI, IUPHAR, MIRBASE, NCBI_PROTEIN, EMBL, COMPOUND, PUBCEM_COMPOUND
    :param file: File name to save the analysis results to
    :param save: Boolean value if true - saves data frame as csv file. default is set to false.
    :param chunk_size: Python generator iter_content() chunk size - default set to 128
    :return: Saves the result as csv file or returns a pandas data frame
    """

    headers = {
        'accept': 'text/csv',
    }

    try:
        response = requests.get(
            'https://reactome.org/AnalysisService/download/%s/pathways/%s/%s' % (token, resource, file),
            headers=headers)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        if save:
            with open("".join([path, file]), 'wb') as f:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    f.write(chunk)
        else:
            lines = csv.reader(response.text.splitlines(), delimiter=',')
            row_list = list(lines)
            df = pandas.DataFrame(row_list)
            df.columns = df.iloc[0]
            df = df.iloc[1:]
            return df
    else:
        print('Status code returned a value of %s' % response.status_code)


def found_entities(token, path='', resource='TOTAL', file='result.csv', save=False, chunk_size=128):
    """
    list of found entities in reactome database

    :param token: The token associated with the data result - analysis Web-Service is token based so for every analysis
        request a TOKEN is associated to the result
    :param path: Absolute path to save the csv file to
    :param resource: The resource to sort TOTAL, UNIPORT, ENSEMBLE, CHEMBI, IUPHAR, MIRBASE, NCBI_PROTEIN, EMBL, COMPOUND, PUBCEM_COMPOUND
    :param file: File name default is set to result.csv
    :param save: If true saves the result data frame as csv file, else it returns the data frame
    :param chunk_size: Python generator iter_content() chunk size - default set to 128
    :return: Pandas data frame with genes or entities found in pathway enrichment analysis overlap
    """

    headers = {
        'accept': 'text/csv',
    }

    try:
        response = requests.get(
            'https://reactome.org/AnalysisService/download/%s/entities/found/%s/%s' % (token, resource, file),
            headers=headers)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        if save:
            with open("".join([path, file]), 'wb') as f:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    f.write(chunk)
        else:
            gene_list = response.text.split('\n')
            df_list = [row.split(",") for row in gene_list[:-1]]
            df = pandas.DataFrame(df_list)
            df = df.iloc[1:]
            return df
    else:
        print('Status code returned a value of %s' % response.status_code)


def unfound_entities(token, path='', file='result.csv', save=False, chunk_size=128):
    """
    list of unfound entities in reactome database

    :param token: The token associated with the data result - analysis Web-Service is token based, so for every analysis
        request a TOKEN is associated to the result
    :param file: File name default is set to result.csv
    :param path: Absolute path to save the csv file to
    :param save:  If true saves the result data frame as csv file, else it returns the data frame
    :param chunk_size: Python generator iter_content() chunk size - default set to 128
    :return: Pandas data frame with genes or entities not found in pathway enrichment analysis overlap
    """

    headers = {
        'accept': 'text/csv',
    }

    try:
        response = requests.get(
            'https://reactome.org/AnalysisService/download/%s/entities/notfound/%s' % (token, file),
            headers=headers)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        if save:
            with open("".join([path, file]), 'wb') as f:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    f.write(chunk)
        else:
            gene_list = response.text.split('\n')
            df_list = [row.split(",") for row in gene_list[:-1]]
            df = pandas.DataFrame(df_list)
            df = df.iloc[1:]
            return df
    else:
        print('Status code returned a value of %s' % response.status_code)


def db_name():
    """
    The name of current database

    :return: String of the name of current database.
    """

    headers = {
        'accept': 'text/plain',
    }

    try:
        response = requests.get('https://reactome.org/AnalysisService/database/name', headers=headers)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.text
    else:
        print('Status code returned a value of %s' % response.status_code)


def db_version():
    """
    The version number of current database

    :return: String of the version number of current database.
    """

    headers = {
        'accept': 'text/plain',
    }

    try:
        response = requests.get('https://reactome.org/AnalysisService/database/version', headers=headers)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.text
    else:
        print('Status code returned a value of %s' % response.status_code)


def report(token, path, file='report.pdf', number='25', resource='TOTAL', diagram_profile='Modern', analysis_profile='Standard',
                fireworks_profile='Barium Lithium', species='Homo sapiens', chunk_size=128):
    """
    Downloads a report for a given pathway analysis result

    :param token: The token associated with the data result - analysis Web-Service is token based, so for every analysis
        request a TOKEN is associated to the result
    :param path: Absolute path to save the report pdf file to
    :param file: Pdf file name to save the analysis report to - default set to report.pdf
    :param number: Number of pathways reported (max 50)
    :param resource: The resource to sort TOTAL, UNIPORT, ENSEMBLE, CHEMBI, IUPHAR, MIRBASE, NCBI_PROTEIN, EMBL, COMPOUND, PUBCEM_COMPOUND
    :param diagram_profile: Diagram Color Profile - as string
    :param analysis_profile: Analysis Color Profile - as string
    :param fireworks_profile: Diagram Color Profile - as string
    :param species: The species for which results will be reported
    :param chunk_size: Python generator iter_content() chunk size - default set to 128
    :return: Saves a reactome analysis pdf report to the indicated path and file name
    """

    if isinstance(number, NumberTypes):
        number = str(number)

    headers = {
        'accept': 'application/pdf',
    }

    params = (
        ('number', number),
        ('resource', resource),
        ('diagramProfile', diagram_profile),
        ('analysisProfile', analysis_profile),
        ('fireworksProfile', fireworks_profile),
    )

    try:
        response = requests.get('https://reactome.org/AnalysisService/report/%s/%s/%s' % (token, species, file),
                                headers=headers, params=params)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        with open("".join([path, file]), 'wb') as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                f.write(chunk)
    else:
        print('Status code returned a value of %s' % response.status_code)


def compare_species(species='48892', page_size='1', page='1', sort_by='ENTITIES_FDR', order='ASC',
                    resource='TOTAL', p_value='1'):
    """
    Compares Homo sapiens to the specified species

    :param species: The reactome dbId string of the species to compare to ex. of some dbId mappings {'Homo sapiens':'48887',
        'Mus musculus':'48892', 'Rattus norvegicus':'48895', 'Sus scrofa':'49633', 'Xenopus tropicalis':'205621',
        'Bos taurus':'48898', 'Gallus gallus':'49591'}
    :param page_size: Page size
    :param page: Number of pages
    :param sort_by: How to sort the result. Available filters: TOTAL_ENTITIES, TOTAL_REACTIONS, TOTAL_INTERACTIONS,
        FOUND_ENTITIES, FOUND_INTERACTIONS, FOUND_REACTIONS, ENTITIES_RATIO, ENTITIES_PVALUE, ENTITIES_FDR, REACTIONS_RATIO
    :param order: Order ASC or DESC
    :param resource: The resource to sort TOTAL, UNIPORT, ENSEMBLE, CHEMBI, IUPHAR, MIRBASE, NCBI_PROTEIN, EMBL, COMPOUND, PUBCEM_COMPOUND
    :param p_value: Defines the pValue threshold. Only hit pathway with pValue equals or below the threshold will be returned
    :return: Json dictionary object
    """

    if isinstance(page_size, NumberTypes):
        page_size = str(page_size)

    if isinstance(page, NumberTypes):
        page = str(page)

    if isinstance(p_value, NumberTypes):
        p_value = str(p_value)

    headers = {
        'accept': 'application/json',
    }

    params = (
        ('pageSize', page_size),
        ('page', page),
        ('sortBy', sort_by),
        ('order', order),
        ('species',  species),
        ('resource', resource),
        ('pValue', p_value),
    )

    url = 'https://reactome.org/AnalysisService/species/homoSapiens/%s' % species

    try:
        response = requests.get(url=url, headers=headers, params=params)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print('Status code returned a value of %s' % response.status_code)


def identifiers_mapping(ids='EGF,EGFR', interactors=False, projection=False):
    """
    Maps the identifiers passed as a comma seperated list in str format over the different species and if projection is
    set to true, projects the result to Homo Sapiens

    :param ids: Comma seperated list of proteins, genes or small molecules identifiers symbol in string format ex. 'EGF,EGFR'
    :param interactors: boolean value if set to false, your query will consider only manually curated Reactome pathways
        with known biological significance. if true, your query will consider Reactome pathways that have been expanded by
        including all available protein-protein interactors from the IntAct database.
    :param projection: If true, projects the identifiers to human and only shows the result in this species
    :return: Json list object
    """

    if interactors:
        interactors = 'true'
    else:
        interactors = 'false'

    if projection:
        url = 'https://reactome.org/AnalysisService/mapping/projection'
    else:
        url = 'https://reactome.org/AnalysisService/mapping/'

    headers = {
        'accept': 'application/json',
        'content-type': 'text/plain',
    }

    params = (
        ('interactors', interactors),
    )

    data = ids

    try:
        response = requests.post(url=url, headers=headers, params=params, data=data)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print('Status code returned a value of %s' % response.status_code)


def identifiers_mapping_form(path, interactors=False, projection=False):
    """
    Maps the identifiers passed via txt file over the different species and if projection is set to true, projects the
    result to Homo Sapiens

    :param path: Absolute path to the the txt file with identifier symbols to be analysed -
        refer to https://reactome.org/dev/analysis for format.
    :param interactors: boolean value if set to false, your query will consider only manually curated Reactome pathways
        with known biological significance. if true, your query will consider Reactome pathways that have been expanded by
        including all available protein-protein interactors from the IntAct database.
    :param projection: If true, projects the identifiers to human and only shows the result in this species
    :return:
    """

    if interactors:
        interactors = 'true'
    else:
        interactors = 'false'

    if projection:
        url = 'https://reactome.org/AnalysisService/mapping/form/projection'
    else:
        url = 'https://reactome.org/AnalysisService/mapping/form'

    headers = {
        'Content-Type': 'text/plain',
    }

    params = (
        ('interactors', interactors),
    )

    data = open(path, 'rb').read()

    try:
        response = requests.post(url=url, headers=headers, params=params, data=data)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print("Status code returned a value of %s" % response.status_code)


def identifiers_mapping_url(external_url, interactors=False, projection=False):
    """
    Maps the identifiers passed via url over the different species and if projection is set to true, projects the
    result to Homo Sapiens

    :param external_url:
    :param interactors: Boolean value if set to false, your query will consider only manually curated Reactome pathways
        with known biological significance. if true, your query will consider Reactome pathways that have been expanded by
        including all available protein-protein interactors from the IntAct database.
    :param projection: If true, projects the identifiers to human and only shows the result in this species
    :return:
    """

    if interactors:
        interactors = 'true'
    else:
        interactors = 'false'

    if projection:
        url = 'https://reactome.org/AnalysisService/mapping/url/projection'
    else:
        url = 'https://reactome.org/AnalysisService/mapping/url/'

    headers = {
        'Content-Type': 'text/plain',
    }

    params = (
        ('interactors', interactors),
    )

    data = external_url

    try:
        response = requests.post(url=url, headers=headers, params=params, data=data)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print('Status code returned a value of %s' % response.status_code)


def token(token, species='Homo sapiens', page_size='1', page='1', sort_by='ENTITIES_FDR', order='ASC', resource='TOTAL',
          p_value='1', include_disease=True, min_entities=None, max_entities=None):
    """
    Returns the result associated with token.
    Use page and pageSize to reduce the amount of data retrieved. Use sortBy and order to sort the result by your preferred option.
    The resource field will filter the results to show only those corresponding to the preferred molecule type (TOTAL includes all the different molecules type)

    :param token: The token associated with the data result - analysis Web-Service is token based, so for every analysis
        request a TOKEN is associated to the result
    :param species: List of species to filter the result (accepts taxonomy ids, species names and reactome dbId)
    :param page_size: Page size
    :param page: Page number
    :param sort_by: How to sort the result. Available filters: TOTAL_ENTITIES, TOTAL_REACTIONS, TOTAL_INTERACTIONS,
        FOUND_ENTITIES, FOUND_INTERACTIONS, FOUND_REACTIONS, ENTITIES_RATIO, ENTITIES_PVALUE, ENTITIES_FDR, REACTIONS_RATIO
    :param order: Order ASC or DESC
    :param resource: The resource to sort TOTAL, UNIPORT, ENSEMBLE, CHEMBI, IUPHAR, MIRBASE, NCBI_PROTEIN, EMBL, COMPOUND, PUBCEM_COMPOUND
    :param p_value: Defines the pValue threshold. Only hit pathway with pValue equals or below the threshold will be returned
    :param include_disease: Set to ‘false’ to exclude the disease pathways from the result (it does not alter the statistics)
    :param min_entities: Minimum number of contained entities per pathway (takes into account the resource)
    :param max_entities: Maximum number of contained entities per pathway (takes into account the resource)
    :return: Json dictionary object
    """

    if isinstance(page_size, NumberTypes):
        page_size = str(page_size)

    if isinstance(page, NumberTypes):
        page = str(page)

    if isinstance(p_value, NumberTypes):
        p_value = str(p_value)

    if isinstance(min_entities, NumberTypes):
        min_entities = str(min_entities)

    if isinstance(max_entities, NumberTypes):
        max_entities = str(max_entities)

    if include_disease:
        include_disease = 'true'
    else:
        include_disease = 'false'

    headers = {
        'accept': 'application/json',
    }

    params = (
        ('pageSize', page_size),
        ('page', page),
        ('sortBy', sort_by),
        ('order', order),
        ('species',  species),
        ('resource', resource),
        ('pValue', p_value),
        ('includeDisease', include_disease),
        ('min', min_entities),
        ('max', max_entities),
    )

    url = 'https://reactome.org/AnalysisService/token/%s' % token

    try:
        response = requests.get(url=url, headers=headers, params=params)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print('Status code returned a value of %s' % response.status_code)


def token_pathways_result(token, pathways, species='Homo sapiens', resource='TOTAL', p_value='1', include_disease=True,
                          min_entities=None, max_entities=None):
    """
    For a given list of pathway stable identifiers (stId) it will query and retrieve a list containing those that are
    present in the result (with the results for the indicated molecule type)

    :param token: The token associated with the data result - analysis Web-Service is token based, so for every analysis
        request a TOKEN is associated to the result
    :param pathways: The pathways stable identifiers (stId - provided in the analysis result for each pathway)
    :param species: List of species to filter the result (accepts taxonomy ids, species names and reactome dbId)
    :param resource: The resource to sort TOTAL, UNIPORT, ENSEMBLE, CHEMBI, IUPHAR, MIRBASE, NCBI_PROTEIN, EMBL, COMPOUND, PUBCEM_COMPOUND
    :param p_value: Defines the pValue threshold. Only hit pathway with pValue equals or below the threshold will be returned
    :param include_disease: Set to ‘false’ to exclude the disease pathways from the result (it does not alter the statistics)
    :param min_entities: Minimum number of contained entities per pathway (takes into account the resource)
    :param max_entities: Maximum number of contained entities per pathway (takes into account the resource)
    :return: Json list object
    """
    if isinstance(p_value, NumberTypes):
        p_value = str(p_value)

    if isinstance(min_entities, NumberTypes):
        min_entities = str(min_entities)

    if isinstance(max_entities, NumberTypes):
        max_entities = str(max_entities)

    if include_disease:
        include_disease = 'true'
    else:
        include_disease = 'false'

    headers = {
        'accept': 'application/json',
        'content-type': 'text/plain',
    }

    params = (
        ('species',  species),
        ('resource', resource),
        ('pValue', p_value),
        ('includeDisease', include_disease),
        ('min', min_entities),
        ('max', max_entities),
    )

    url = 'https://reactome.org/AnalysisService/token/%s/filter/pathways' % token

    data = pathways

    try:
        response = requests.post(url=url, headers=headers, params=params, data=data)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print('Status code returned a value of %s' % response.status_code)


def token_filter_species(token, species='Homo sapiens', sort_by='ENTITIES_FDR', order='ASC', resource='TOTAL'):
    """
    Queries analysis token and returns and filters the result by species

    :param token: The token associated with the data result - analysis Web-Service is token based, so for every analysis
        request a TOKEN is associated to the result
    :param species: List of species to filter the result (accepts taxonomy ids, species names and reactome dbId)
    :param sort_by: How to sort the result. Available filters: TOTAL_ENTITIES, TOTAL_REACTIONS, TOTAL_INTERACTIONS,
        FOUND_ENTITIES, FOUND_INTERACTIONS, FOUND_REACTIONS, ENTITIES_RATIO, ENTITIES_PVALUE, ENTITIES_FDR, REACTIONS_RATIO
    :param order: Order ASC or DESC
    :param resource: The resource to sort TOTAL, UNIPORT, ENSEMBLE, CHEMBI, IUPHAR, MIRBASE, NCBI_PROTEIN, EMBL, COMPOUND, PUBCEM_COMPOUND
    :return: Json dictionary object
    """

    headers = {
        'accept': 'application/json',
    }

    params = (
        ('sortBy', sort_by),
        ('order', order),
        ('resource', resource),
    )

    url = 'https://reactome.org/AnalysisService/token/%s/filter/species/%s' % (token, species)

    try:
        response = requests.get(url=url, headers=headers, params=params)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print("Status code returned a value of %s" % response.status_code)


def token_pathways_summary(token, pathways, resource='TOTAL'):
    """
    Queries analysis token and returns a summary of the contained identifiers and interactors for all pathways

    :param token: The token associated with the data result - analysis Web-Service is token based, so for every analysis
        request a TOKEN is associated to the result
    :param pathways: The pathways stable identifier (stId - provided in the analysis result for each pathway)
    :param resource: The resource to sort TOTAL, UNIPORT, ENSEMBLE, CHEMBI, IUPHAR, MIRBASE, NCBI_PROTEIN, EMBL, COMPOUND, PUBCEM_COMPOUND
    :return: Json list object
    """

    headers = {
        'accept': 'application/json',
        'content-type': 'text/plain',
    }

    params = (
        ('resource', resource),
    )

    data = pathways
    url = 'https://reactome.org/AnalysisService/token/%s/found/all' % token

    try:
        response = requests.post(url=url, headers=headers, params=params, data=data)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print("Status code returned a value of %s" % response.status_code)


def token_pathway_summary(token, pathway, resource='TOTAL', page='1', page_size='1', by='all'):
    """
    Queries analysis token and returns a summary of
        1. by='all': all the contained identifiers and interactors
        2. by='entities': the found curated identifiers
        3. by='interactors': the found interactors (may return null or none)

    for a given pathway and token

    :param token: The token associated with the data result - analysis Web-Service is token based, so for every analysis
        request a TOKEN is associated to the result
    :param pathway: The pathway stable identifier (stId - provided in the analysis result for each pathway)
    :param resource: The resource to sort TOTAL, UNIPORT, ENSEMBLE, CHEMBI, IUPHAR, MIRBASE, NCBI_PROTEIN, EMBL, COMPOUND, PUBCEM_COMPOUND
    :param page: Page number
    :param page_size: Page size
    :param by: Filter found cases by: all, entities, interactors
    :return: Json dictionary object
    """

    if isinstance(page_size, NumberTypes):
        page_size = str(page_size)

    if isinstance(page, NumberTypes):
        page = str(page)

    headers = {
        'accept': 'application/json',
    }

    if by.lower() in 'all':
        params = (
            ('resource', resource),
        )

        url = 'https://reactome.org/AnalysisService/token/%s/found/all/%s' % (token, pathway)

    elif by.lower() in 'entities':
        params = (
            ('resource', resource),
            ('page', page),
            ('pageSize', page_size),
        )

        url = 'https://reactome.org/AnalysisService/token/%s/found/entities/%s' % (token, pathway)

    elif by.lower() in 'interactors':
        params = (
            ('resource', resource),
            ('page', page),
            ('pageSize', page_size),
        )

        url = 'https://reactome.org/AnalysisService/token/%s/found/interactors/%s' % (token, pathway)

    try:
        response = requests.get(url=url, headers=headers, params=params)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print('Status code returned a value of %s' % response.status_code)


def token_unfound_identifiers(token, page_size='1', page='1'):
    """
    Returns a list of the identifiers not found for a given token

    :param token: The token associated with the data result - analysis Web-Service is token based, so for every analysis
        request a TOKEN is associated to the result
    :param page_size: Page size
    :param page: Number of pages
    :return: list
    """

    if isinstance(page_size, NumberTypes):
        page_size = str(page_size)

    if isinstance(page, NumberTypes):
        page = str(page)

    headers = {
        'accept': 'application/json',
    }

    params = (
        ('pageSize', page_size),
        ('page', page),
    )
    url = 'https://reactome.org/AnalysisService/token/%s/notFound' % token

    try:
        response = requests.get(url=url, headers=headers, params=params)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print('Status code returned a value of %s' % response.status_code)


def token_pathway_page(token, pathway, page_size='1', sort_by='ENTITIES_FDR', order='ASC', resource='TOTAL', p_value='1',
                       include_disease=True, min_entities=None, max_entities=None):
    """
    Returns the page where the corresponding pathway is taking into account the passed parameters

    :param token: The token associated with the data result - analysis Web-Service is token based, so for every analysis
        request a TOKEN is associated to the result
    :param pathway: The pathway stable identifier (stId - provided in the analysis result for each pathway)
    :param page_size: Page size
    :param sort_by: How to sort the result. Available filters: TOTAL_ENTITIES, TOTAL_REACTIONS, TOTAL_INTERACTIONS,
        FOUND_ENTITIES, FOUND_INTERACTIONS, FOUND_REACTIONS, ENTITIES_RATIO, ENTITIES_PVALUE, ENTITIES_FDR, REACTIONS_RATIO
    :param order: Order ASC or DESC
    :param resource: The resource to sort TOTAL, UNIPORT, ENSEMBLE, CHEMBI, IUPHAR, MIRBASE, NCBI_PROTEIN, EMBL, COMPOUND, PUBCEM_COMPOUND
    :param p_value: Defines the pValue threshold. Only hit pathway with pValue equals or below the threshold will be returned
    :param include_disease: Set to ‘false’ to exclude the disease pathways from the result (it does not alter the statistics)
    :param min_entities: Minimum number of contained entities per pathway (takes into account the resource)
    :param max_entities: Maximum number of contained entities per pathway (takes into account the resource)
    :return: int
    """

    if isinstance(page_size, NumberTypes):
        page_size = str(page_size)

    if isinstance(p_value, NumberTypes):
        p_value = str(p_value)

    if isinstance(min_entities, NumberTypes):
        min_entities = str(min_entities)

    if isinstance(max_entities, NumberTypes):
        max_entities = str(max_entities)

    if include_disease:
        include_disease = 'true'
    else:
        include_disease = 'false'

    headers = {
        'accept': 'application/json',
    }

    params = (
        ('pageSize', page_size),
        ('sortBy', sort_by),
        ('order', order),
        ('resource', resource),
        ('pValue', p_value),
        ('includeDisease', include_disease),
        ('min', min_entities),
        ('max', max_entities),
    )

    url = 'https://reactome.org/AnalysisService/token/%s/page/%s' % (token, pathway)

    try:
        response = requests.get(url=url, headers=headers, params=params)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print('Status code returned a value of %s' % response.status_code)


def token_pathways_binned(token, resource='TOTAL', bin_size='100', p_value='1', include_disease=True):
    """
    Returns a list of binned hit pathway sizes associated with the token

    :param token: The token associated with the data result - analysis Web-Service is token based, so for every analysis
        request a TOKEN is associated to the result
    :param resource: The resource to sort TOTAL, UNIPORT, ENSEMBLE, CHEMBI, IUPHAR, MIRBASE, NCBI_PROTEIN, EMBL, COMPOUND, PUBCEM_COMPOUND
    :param bin_size: Defines the size of each bin for the classification (min: 100)
    :param p_value: Defines the pValue threshold. Only hit pathway with pValue equals or below the threshold will be returned
    :param include_disease: Set to ‘false’ to exclude the disease pathways from the result (it does not alter the statistics)
    :return: Json list object
    """

    if isinstance(bin_size, NumberTypes):
        bin_size = str(bin_size)

    if isinstance(p_value, NumberTypes):
        p_value = str(p_value)

    if include_disease:
        include_disease = 'true'
    else:
        include_disease = 'false'

    headers = {
        'accept': 'application/json',
    }

    params = (
        ('resource', resource),
        ('binSize', bin_size),
        ('pValue', p_value),
        ('includeDisease', include_disease),
    )

    url = 'https://reactome.org/AnalysisService/token/%s/pathways/binned' % token

    try:
        response = requests.get(url=url, headers=headers, params=params)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print('Status code returned a value of %s' % response.status_code)


def token_pathways_reactions(token, pathways, resource='TOTAL', p_value='1', include_disease=True, min_entities=None,
                             max_entities=None):
    """
    Returns the reaction ids of all the pathway stable identifiers (stIds) that are present in the original result

    :param token: The token associated with the data result - analysis Web-Service is token based, so for every analysis
        request a TOKEN is associated to the result
    :param pathways: The pathways stable identifier (stId - provided in the analysis result for each pathway)
    :param resource: The resource to sort TOTAL, UNIPORT, ENSEMBLE, CHEMBI, IUPHAR, MIRBASE, NCBI_PROTEIN, EMBL, COMPOUND, PUBCEM_COMPOUND
    :param p_value: Defines the pValue threshold. Only hit pathway with pValue equals or below the threshold will be returned
    :param include_disease: Set to ‘false’ to exclude the disease pathways from the result (it does not alter the statistics)
    :param min_entities: Minimum number of contained entities per pathway (takes into account the resource)
    :param max_entities: Maximum number of contained entities per pathway (takes into account the resource)
    :return: list
    """

    if isinstance(p_value, NumberTypes):
        p_value = str(p_value)

    if isinstance(min_entities, NumberTypes):
        min_entities = str(min_entities)

    if isinstance(max_entities, NumberTypes):
        max_entities = str(max_entities)

    if include_disease:
        include_disease = 'true'
    else:
        include_disease = 'false'

    headers = {
        'accept': 'application/json',
        'content-type': 'text/plain',
    }

    params = (
        ('resource', resource),
        ('pValue', p_value),
        ('includeDisease', include_disease),
        ('min', min_entities),
        ('max', max_entities),
    )

    data = pathways

    url = 'https://reactome.org/AnalysisService/token/%s/reactions/pathways' % token

    try:
        response = requests.post(url=url, headers=headers, params=params, data=data)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print("Status code returned a value of %s" % response.status_code)


def token_pathway_reactions(token, pathway, resource='TOTAL', p_value='1', include_disease=True, min_entities=None,
                             max_entities=None):
    """
    Returns the reaction ids a or one pathway's stable identifiers (stId) that is present in the original result

    :param token: The token associated with the data result - analysis Web-Service is token based, so for every analysis
        request a TOKEN is associated to the result
    :param pathway: The pathway stable identifier (stId - provided in the analysis result for each pathway)
    :param resource: The resource to sort TOTAL, UNIPORT, ENSEMBLE, CHEMBI, IUPHAR, MIRBASE, NCBI_PROTEIN, EMBL, COMPOUND, PUBCEM_COMPOUND
    :param p_value: Defines the pValue threshold. Only hit pathway with pValue equals or below the threshold will be returned
    :param include_disease: Set to ‘false’ to exclude the disease pathways from the result (it does not alter the statistics)
    :param min_entities: Minimum number of contained entities per pathway (takes into account the resource)
    :param max_entities: Maximum number of contained entities per pathway (takes into account the resource)
    :return: list
    """

    if isinstance(p_value, NumberTypes):
        p_value = str(p_value)

    if isinstance(min_entities, NumberTypes):
        min_entities = str(min_entities)

    if isinstance(max_entities, NumberTypes):
        max_entities = str(max_entities)

    if include_disease:
        include_disease = 'true'
    else:
        include_disease = 'false'

    headers = {
        'accept': 'application/json',
    }

    params = (
        ('resource', resource),
        ('pValue', p_value),
        ('includeDisease', include_disease),
        ('min', min_entities),
        ('max', max_entities),
    )

    url = 'https://reactome.org/AnalysisService/token/%s/reactions/%s' % (token, pathway)

    try:
        response = requests.get(url=url, headers=headers, params=params)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print('Status code returned a value of %s' % response.status_code)


def token_resources(token):
    """
    the resources summary associated with the token

    :param token: The token associated with the data result - analysis Web-Service is token based, so for every analysis
        request a TOKEN is associated to the result
    :return: Json list object
    """

    headers = {
        'accept': 'application/json',
    }

    url = 'https://reactome.org/AnalysisService/token/%s/resources' % token

    try:
        response = requests.get(url=url, headers=headers)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print('Status code returned a value of %s' % response.status_code)


def import_json(input_json):
    """
    Imports the posted json into the service
    The accepted format is the same as provided by the method /#/download/{token}/result.json. Note: The provided file can be gzipped.

    :param input_json: Identifiers to analyse followed by their expression (when applies) in json format in string
    :return:
    """

    headers = {
        'accept': 'application/json',
        'content-type': 'application/json',
    }

    data = input_json

    url = 'https://reactome.org/AnalysisService/import/'

    try:
        response = requests.post(url=url, headers=headers, data=data)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print("Status code returned a value of %s" % response.status_code)


def import_form(input_file):
    """
    Imports the posted json file into the service
    The accepted format is the same as provided by the method /#/download/{token}/result.json. Note: The submitted file can be gzipped.

    :param input_file: A json file with the data to be analysed
    :return:
    """

    headers = {
        'content-type': 'application/json',
    }

    data = input_file

    url = 'https://reactome.org/AnalysisService/import/form'

    try:
        response = requests.post(url=url, headers=headers, data=data)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print("Status code returned a value of %s" % response.status_code)


def import_url(input_url):
    """
    Imports the json file provided by the posted url into the service
    The accepted format is the same as provided by the method /#/download/{token}/result.json. Note: The provided file can be gzipped.

    :param input_url: A URL pointing to the json data to be analysed
    :return:
    """

    headers = {
        'content-type': 'application/json',
    }

    data = input_url

    url = 'https://reactome.org/AnalysisService/import/url'

    try:
        response = requests.post(url=url, headers=headers, data=data)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print("Status code returned a value of %s" % response.status_code)

