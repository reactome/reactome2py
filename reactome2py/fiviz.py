"""
 Human functional protein interactions (FI) services api calls
 and utility functions for Reactome data-fetch, mappings, and overlay networks in human.
"""
import io
import tarfile
import zipfile
from typing import *

import requests
from requests.exceptions import ConnectionError

from . import util

_CPWS = "http://cpws.reactome.org/caBigR3WebApp"


def ehld_stids() -> List[str]:
    """
    Retrieves a list of high-level hierarchy pathway with Enhanced High Level Diagrams (EHLD) https://reactome.org/icon-info/ehld-specs-guideline

    :return: list of pathway stIds
    """
    return [
        stId for stId in util.get("https://reactome.org/download/current/ehld/svgsummary.txt").text.splitlines()
        if 'R-' in stId
    ]


def sbgn_stids():
    """
    Retieves a list of lower-level (with hierarchy) pathways that have SBGNs https://reactome.org/about/news/110-sbgn-files-revamp

    :return: list of pathway stIds
    """

    url = "https://reactome.org/download/current/homo_sapiens.sbgn.tar.gz"

    try:
        response = requests.get(url=url)
        if response.status_code == 200:
            tar_file = tarfile.open(fileobj=io.BytesIO(response.content))
            file_names = tar_file.getnames()
            ehlds = ehld_stids()
            sbgns = [f.replace('.sbgn', '').replace('./', '') for f in file_names]

            sbgn_only = list(set(sbgns) - set(ehlds))
            return sbgn_only
        else:
            print(f'Status code returned a value of {response.status_code}')
    except ConnectionError as e:
        print(e)


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
        if response.status_code == 200:
            gm = _read_ziplines(response)
            relations = []

            for i, e in enumerate(gm):
                gm[i] = [s.strip() for s in gm[i]]
                d = dict(name=gm[i][0], stId=gm[i][1], genes=gm[i][2:len(gm[i])])
                relations.append(d)

            return relations
        else:
            print(f'Status code returned a value of {response.status_code}')
    except ConnectionError as e:
        print(e)


def pathway_fi(release="2019", st_id="R-HSA-177929", pattern="R-HSA-"):
    """
    Fetch Pathway's Functional Interactions (FI) https://www.ncbi.nlm.nih.gov/pubmed/20482850

    :param release: release year for Functional Interactions (FI) data
    :param st_id: stable Identifier (stID) of a pathway
    :param pattern: reactome's stable Identifier (stID) string tag for Human "R-HSA-"

    :return: json dictionary object
    """

    return util.get_json(f'{_CPWS}{release}/FIService/network/convertPathwayToFIs/{st_id.replace(pattern, "")}')


def genelist_fi(release="2019", ids="EGF,EGFR"):
    """
    Fetch Pathway's genelist Functional Interactions (FI) https://www.ncbi.nlm.nih.gov/pubmed/20482850

    :param release: release year for Functional Interactions (FI) data
    :param ids: String of comma separated Gene names (HGNC)

    :return: json dictionary object
    """
    return util.post_json(f"{_CPWS}{release}/FIService/network/queryEdge", data=ids.replace(',', '\t'))


def pathway_boolean_network(release="2019", st_id="R-HSA-177929", pattern="R-HSA-"):
    """
    Fetch Pathway as a boolean network

    :param release: release year for Functional Interactions (FI) data
    :param st_id: stable Identifier (stID) of a pathway
    :param pattern: reactome's stable Identifier (stID) string tag for Human "R-HSA-"

    :return: json dictionary object
    """
    db_id = st_id.replace(pattern, "")
    return util.get_json(f'{_CPWS}{release}/FIService/network/convertPathwayToBooleanNetwork/{db_id}')


def pathway_factor_graph(release="2019", st_id="R-HSA-177929", pattern="R-HSA-"):
    """
    Fetch Pathway as a factor graph

    :param release: release year for Functional Interactions (FI) data
    :param st_id: stable Identifier (stID) of a pathway
    :param pattern: reactome's stable Identifier (stID) string tag for Human "R-HSA-"

    :return: json dictionary object
    """
    db_id = st_id.replace(pattern, "")
    return util.post_json(f'{_CPWS}{release}/FIService/network/convertPathwayToFactorGraph/{db_id}', data="")


def drug_data_source(release="2019", source="drugcentral"):
    """
    Query a list of drug-target interactions from targetome or drugcentral

    :param release: release year for Functional Interactions (FI) data
    :param source: drugcentral or targetome

    :return: json dictionary object
    """
    return util.get_json(f'{_CPWS}{release}/FIService/drug/listDrugs/{source}')


def genelist_drug_target(release="2019", ids="EGFR,ESR1,BRAF", source="drugcentral"):
    """
    Query drug-target interactions for a gene list from targetome or drugcentral

    :param release: release year for Functional Interactions (FI) data
    :param ids: String of comma separated Gene names (HGNC)
    :param source: drugcentral or targetome

    :return: json dictionary object
    """
    return util.post_json(
        f'{_CPWS}{release}/FIService/drug/queryDrugTargetInteractions/{source}',
        data=ids.replace(",", "\n")
    )


def pathway_pe_drug_target(release="2019", source="drugcentral", pd_id="507988", pe_id="1220578", pattern="R-HSA-"):
    """
    Query drug-target interactions for a Physical Entity ex a complex within a pathway

    :param release: release year for Functional Interactions (FI) data
    :param source: drugcentral or targetome
    :param pd_id: stable Identifier (stID) of a pathway
    :param pe_id: stable Identifier (stID) of a PhysicalEntity ex. EGF:Ligand-responsive R-HSA-1220578' within human context

    :return: json dictionary object
    """
    pd_id = pd_id.replace(pattern, "")
    pe_id = pe_id.replace(pattern, "")
    ids = "/".join([pd_id, pe_id])

    return util.get_json(
        f"{_CPWS}{release}/FIService/drug/queryInteractionsForPEInDiagram/{source}/{ids}"
    )


def pathway_drug_target(release="2019", source="drugcentral", pd_id="507988", pattern="R-HSA-"):
    """
    Query drug-target interactions for a  PhysicalEntity

    :param release: release year for Functional Interactions (FI) data
    :param source: drugcentral or targetome
    :param pd_id: stable Identifier (stID) of a pathway

    :return: json dictionary object
    """
    pd_id = pd_id.replace(pattern, "")
    return util.get_json(f'{_CPWS}{release}/FIService/drug/queryInteractionsForDiagram/{source}/{pd_id}')


def drug_targets(release="2019", drug="Gefitinib", source="drugcentral"):
    """
    Query known/available drug-target interactions for a drug

    :param release: release year for Functional Interactions (FI) data
    :param source: drugcentral or targetome

    :return: json dictionary object
    """
    return util.post_json(f'{_CPWS}{release}/FIService/drug/queryInteractionsForDrugs/{source}', data=drug)
