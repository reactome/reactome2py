from reactome2py import content


def test_discover():
    assert type(content.discover()) == dict


def test_disease():
    assert type(content.disease()) == list
