from reactome2py import fiviz


def test_ehld_stids():
    assert isinstance(fiviz.ehld_stids(), list)


def test_sbgn_stids():
    assert isinstance(fiviz.sbgn_stids(), list)


def test_sbgn_notin_ehld():
    sbgn_stIds = fiviz.sbgn_stids()
    ehld_stIds = fiviz.ehld_stids()
    is_subset = set(sbgn_stIds).intersection(ehld_stIds)
    assert bool(is_subset) is False


def test_gene_mappings():
    assert isinstance(fiviz.gene_mappings()[0], dict)


def test_pathway_fi():
    assert isinstance(fiviz.pathway_fi(), dict)


def test_genelist_fi():
    assert isinstance(fiviz.genelist_fi(), dict)


def test_pathway_boolean_network():
    assert isinstance(fiviz.pathway_boolean_network(), dict)


def test_pathway_factor_graph():
    assert isinstance(fiviz.pathway_factor_graph(), dict)


def test_drug_data_source():
    assert isinstance(fiviz.drug_data_source(), dict)


def test_genelist_drug_target():
    assert isinstance(fiviz.genelist_drug_target(), dict)


def test_pathway_pe_drug_target():
    assert isinstance(fiviz.pathway_pe_drug_target(), dict)


def test_pathway_drug_target():
    assert isinstance(fiviz.pathway_drug_target(), dict)


def test_drug_targets():
    assert isinstance(fiviz.drug_targets(), dict)
