from reactome2py import utils


def test_ehld_stids():
    assert isinstance(utils.ehld_stids(), list)


def test_sbgn_stids():
    assert isinstance(utils.sbgn_stids(), list)


def test_gene_mappings():
    assert isinstance(utils.gene_mappings()[0], dict)
