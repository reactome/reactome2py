from reactome2py import analysis


def test_identifier():
    assert type(analysis.identifier()) == dict


def test_identifiers():
    assert type(analysis.identifiers()) == dict


