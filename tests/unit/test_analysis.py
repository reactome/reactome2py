from reactome2py import analysis
import pandas
import pytest

markers = 'EGFR,STAT'
result = analysis.identifiers(ids=markers)
token = result['summary']['token']
pytest.global_variable_token = token


def test_identifier():
    assert type(analysis.identifier()) == dict


def test_identifiers():
    assert type(analysis.identifiers()) == dict


def test_result2json():
    token = pytest.global_variable_token
    assert type(analysis.result2json(token)) == dict


def test_pathway2df():
    token = pytest.global_variable_token
    df = analysis.pathway2df(token)
    assert type(df) == pandas.core.frame.DataFrame


def test_found_entities():
    token = pytest.global_variable_token
    df = analysis.found_entities(token)
    assert type(df) == pandas.core.frame.DataFrame


def test_unfound_entities():
    token = pytest.global_variable_token
    df = analysis.unfound_entities(token)
    assert type(df) == pandas.core.frame.DataFrame


def test_db_name():
    assert type(analysis.db_name()) == str


def test_db_version():
    assert type(analysis.db_version()) == str


def test_compare_species():
    assert type(analysis.compare_species()) == dict


def test_identifiers_mapping():
    assert type(analysis.identifiers_mapping()) == list


def test_token():
    token = pytest.global_variable_token
    assert type(analysis.token(token)) == dict


def test_token_pathways_result():
    token = pytest.global_variable_token
    assert type(analysis.token_pathways_result(token, pathways='R-HSA-8866910')) == list


def test_token_filter_species():
    token = pytest.global_variable_token
    assert type(analysis.token_filter_species(token)) == dict


def test_token_pathways_summary():
    token = pytest.global_variable_token
    assert type(analysis.token_pathways_summary(token, pathways='R-HSA-8866910')) == list


def test_token_pathway_summary():
    token = pytest.global_variable_token
    assert type(analysis.token_pathway_summary(token, pathway='R-HSA-8866910', resource='TOTAL', page='-1', page_size='-1', by='all')) == dict


def test_token_unfound_identifiers():
    token = pytest.global_variable_token
    assert type(analysis.token_unfound_identifiers(token)) == list


def test_token_pathway_page():
    token = pytest.global_variable_token
    assert type(analysis.token_pathway_page(token, pathway='R-HSA-8866910')) == int


def test_token_pathways_binned():
    token = pytest.global_variable_token
    assert type(analysis.token_pathways_binned(token)) == list


def test_token_pathways_reactions():
    token = pytest.global_variable_token
    assert type(analysis.token_pathways_reactions(token, pathways='R-HSA-8866910')) == list


def test_token_pathway_reactions():
    token = pytest.global_variable_token
    assert type(analysis.token_pathway_reactions(token, pathway='R-HSA-8866910')) == list


def test_token_resources():
    token = pytest.global_variable_token
    assert type(analysis.token_resources(token)) == list
