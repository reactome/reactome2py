"""
Utility functions for Reactome data-fetch, mappings, and overlay networks in human.
"""
from requests.exceptions import ConnectionError
import requests
import io
import tarfile
import zipfile


def ehld_stids():
    """
    Retrieves a list of high-level hierarchy pathway with Enhanced High Level Diagrams (EHLD) https://reactome.org/icon-info/ehld-specs-guideline

    :return: list of pathway stIds
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
    Retieves a list of lower-level (with hierarchy) pathways that have SBGNs https://reactome.org/about/news/110-sbgn-files-revamp

    :return: list of pathway stIds
    """

    url = "https://reactome.org/download/current/homo_sapiens.sbgn.tar.gz"

    try:
        response = requests.get(url=url)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        tar_file = tarfile.open(fileobj=io.BytesIO(response.content))
        file_names = tar_file.getnames()
        ehlds = ehld_stids()
        sbgns = [f.replace('.sbgn', '').replace('./', '') for f in file_names]

        sbgn_only = list(set(sbgns) - set(ehlds))
        return sbgn_only
    else:
        print('Status code returned a value of %s' % response.status_code)


def _yield_zip(response):
    """
    Read zipfile in memory https://docs.python.org/3/library/zipfile.html

    :param response:
    :return: content of zip file
    """

    with zipfile.ZipFile(io.BytesIO(response.content)) as the_zip:
        for zip_info in the_zip.infolist():
            with the_zip.open(zip_info) as the_file:
                yield the_file.readlines()


def _read_ziplines(response):
    """
    Helper function to clean zipline content parsing

    :param response:
    :return: list
    """

    return [c.split('\t') for c in [c.decode('utf8') for c in list(_yield_zip(response))[0]]]


def gene_mappings():
    """
    Maps reactome pathway stId and name to it's associated gene list (HGNC)

    :return: dictionary of reactome pathways and HGNC gene mappings to the pathway.
    """

    url = "https://reactome.org/download/current/ReactomePathways.gmt.zip"

    try:
        response = requests.get(url=url)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        gm = _read_ziplines(response)
        relations = []

        for i, e in enumerate(gm):
            gm[i] = [s.strip() for s in gm[i]]
            d = dict(name=gm[i][0], stId=gm[i][1], genes=gm[i][2:len(gm[i])])
            relations.append(d)

        return relations
    else:
        print('Status code returned a value of %s' % response.status_code)


def pathway_fi(release="2019", stId="R-HSA-177929", pattern="R-HSA-"):
    """
    Fetch Pathway's Functional Interactions (FI) https://www.ncbi.nlm.nih.gov/pubmed/20482850

    :param release: release year for Functional Interactions (FI) data
    :param stId: stable Identifier (stID) of a pathway
    :param pattern: reactome's stable Identifier (stID) string tag for Human "R-HSA-"

    :return: json dictionary object
    """

    headers = {
        'accept': 'application/json',
    }

    if pattern in stId:
        stId = stId.replace(pattern, "")

    url = "http://cpws.reactome.org/caBigR3WebApp%s/FIService/network/convertPathwayToFIs/%s" % (release, stId)

    try:
        response = requests.get(url=url, headers=headers)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print('Status code returned a value of %s' % response.status_code)


def genelist_fi(release="2019", ids="EGF,EGFR"):
    """
    Fetch Pathway's genelist Functional Interactions (FI) https://www.ncbi.nlm.nih.gov/pubmed/20482850

    :param release: release year for Functional Interactions (FI) data
    :param ids: String of comma separated Gene names (HGNC)

    :return: json dictionary object
    """

    headers = {
        'accept': 'application/json',
    }

    if "," in ids:
        ids = ids.replace(",", "\t")

    data = ids

    url = "http://cpws.reactome.org/caBigR3WebApp%s/FIService/network/queryEdge" % release

    try:
        response = requests.post(url=url, headers=headers, data=data)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print("Status code returned a value of %s" % response.status_code)


def pathway_boolean_network(release="2019", stId="R-HSA-177929", pattern="R-HSA-"):
    """
    Fetch Pathway as a boolean network

    :param release: release year for Functional Interactions (FI) data
    :param stId: stable Identifier (stID) of a pathway
    :param pattern: reactome's stable Identifier (stID) string tag for Human "R-HSA-"

    :return: json dictionary object
    """

    headers = {
        'accept': 'application/json',
    }

    if pattern in stId:
        stId = stId.replace(pattern, "")

    url = "http://cpws.reactome.org/caBigR3WebApp%s/FIService/network/convertPathwayToBooleanNetwork/%s" % (release, stId)

    try:
        response = requests.get(url=url, headers=headers)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print('Status code returned a value of %s' % response.status_code)


def pathway_factor_graph(release="2019", stId="R-HSA-177929", pattern="R-HSA-"):
    """
    Fetch Pathway as a factor graph

    :param release: release year for Functional Interactions (FI) data
    :param stId: stable Identifier (stID) of a pathway
    :param pattern: reactome's stable Identifier (stID) string tag for Human "R-HSA-"

    :return: json dictionary object
    """

    headers = {
        'accept': 'application/json',
    }

    if pattern in stId:
        stId = stId.replace(pattern, "")

    url = "http://cpws.reactome.org/caBigR3WebApp%s/FIService/network/convertPathwayToFactorGraph/%s" % (release, stId)

    try:
        response = requests.post(url=url, headers=headers)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print('Status code returned a value of %s' % response.status_code)


def drug_data_source(release="2019", source="drugcentral"):
    """
    Query a list of drug-target interactions from targetome or drugcentral

    :param release: release year for Functional Interactions (FI) data
    :param source: drugcentral or targetome

    :return: json dictionary object
    """

    headers = {
        'accept': 'application/json',
    }

    url = "http://cpws.reactome.org/caBigR3WebApp%s/FIService/drug/listDrugs/%s" % (release, source)

    try:
        response = requests.get(url=url, headers=headers)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print('Status code returned a value of %s' % response.status_code)


def genelist_drug_target(release="2019", ids="EGFR,ESR1,BRAF", source="drugcentral"):
    """
    Query drug-target interactions for a gene list from targetome or drugcentral

    :param release: release year for Functional Interactions (FI) data
    :param ids: String of comma separated Gene names (HGNC)
    :param source: drugcentral or targetome

    :return: json dictionary object
    """

    headers = {
        'accept': 'application/json',
    }

    if "," in ids:
        ids = ids.replace(",", "\n")

    data = ids

    url = "http://cpws.reactome.org/caBigR3WebApp%s/FIService/drug/queryDrugTargetInteractions/%s" % (release, source)

    try:
        response = requests.post(url=url, headers=headers, data=data)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print("Status code returned a value of %s" % response.status_code)


def pathway_pe_drug_target(release="2019", source="drugcentral", pdId="507988", peId="1220578", pattern="R-HSA-"):
    """
    Query drug-target interactions for a Physical Entity ex a complex within a pathway

    :param release: release year for Functional Interactions (FI) data
    :param source: drugcentral or targetome
    :param pdId: stable Identifier (stID) of a pathway
    :param peId: stable Identifier (stID) of a PhysicalEntity ex. EGF:Ligand-responsive R-HSA-1220578' within human context

    :return: json dictionary object
    """

    headers = {
        'accept': 'application/json',
    }

    if pattern in pdId:
        pdId = pdId.replace(pattern, "")

    if pattern in peId:
        peId = peId.replace(pattern, "")

    ids = "/".join([pdId, peId])

    url = "http://cpws.reactome.org/caBigR3WebApp%s/FIService/drug/queryInteractionsForPEInDiagram/%s/%s" % (release, source, ids)

    try:
        response = requests.get(url=url, headers=headers)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print('Status code returned a value of %s' % response.status_code)


def pathway_drug_target(release="2019", source="drugcentral", pdId="507988", pattern="R-HSA-"):
    """
    Query drug-target interactions for a  PhysicalEntity

    :param release: release year for Functional Interactions (FI) data
    :param source: drugcentral or targetome
    :param pdId: stable Identifier (stID) of a pathway

    :return: json dictionary object
    """

    headers = {
        'accept': 'application/json',
    }

    if pattern in pdId:
        pdId = pdId.replace(pattern, "")

    url = "http://cpws.reactome.org/caBigR3WebApp%s/FIService/drug/queryInteractionsForDiagram/%s/%s" % (release, source, pdId)

    try:
        response = requests.get(url=url, headers=headers)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print('Status code returned a value of %s' % response.status_code)


def drug_targets(release="2019", drug="Gefitinib", source="drugcentral"):
    """
    Query known/available drug-target interactions for a drug

    :param release: release year for Functional Interactions (FI) data
    :param ids: String of comma separated Gene names (HGNC)
    :param source: drugcentral or targetome

    :return: json dictionary object
    """

    headers = {
        'accept': 'application/json',
    }

    data = drug

    url = "http://cpws.reactome.org/caBigR3WebApp%s/FIService/drug/queryInteractionsForDrugs/%s" % (release, source)

    try:
        response = requests.post(url=url, headers=headers, data=data)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print("Status code returned a value of %s" % response.status_code)
