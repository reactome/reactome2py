from reactome2py import utils


def test_ehld_stids():
    assert isinstance(utils.ehld_stids(), list)


def test_sbgn_stids():
    assert isinstance(utils.sbgn_stids(), list)


def test_gene_mappings():
    assert isinstance(utils.gene_mappings()[0], dict)


def test_pathway_fi():
    assert isinstance(utils.pathway_fi(), dict)


def test_genelist_fi():
    assert isinstance(utils.genelist_fi(), dict)


def test_pathway_boolean_network():
    assert isinstance(utils.pathway_boolean_network(), dict)


def test_pathway_factor_graph():
    assert isinstance(utils.pathway_factor_graph(), dict)


def test_drug_data_source():
    assert isinstance(utils.drug_data_source(), dict)


def test_genelist_drug_target():
    assert isinstance(utils.genelist_drug_target(), dict)


def test_pathway_pe_drug_target():
    assert isinstance(utils.pathway_pe_drug_target(), dict)


def test_pathway_drug_target():
    assert isinstance(utils.pathway_drug_target(), dict)


def test_drug_targets():
    assert isinstance(utils.drug_targets(), dict)
