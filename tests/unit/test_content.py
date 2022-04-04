from reactome2py import content


def test_discover():
    assert type(content.discover()) == dict


def test_disease():
    assert type(content.disease()) == list


def test_entities_complex():
    assert type(content.entities_complex()) == list


def test_disease():
    assert type(content.disease()) == list


def test_entities_complex():
    assert type(content.entities_complex()) == list


def test_entities_complexes():
    assert type(content.entities_complexes()) == list


def test_entity_structures():
    assert type(content.entity_structures()) == list


def test_entity_other_form():
    assert type(content.entity_other_form()) == list


def test_event_ancestors():
    assert type(content.event_ancestors()) == list


def test_event_species():
    assert type(content.event_species()) == list

# export methods tested on local env


def test_interactors_psicquic_acc():
    assert type(content.interactors_psicquic_acc()) == dict


def test_interactors_psicquic_accs():
    assert type(content.interactors_psicquic_accs()) == dict


def test_interactors_psicquic_resources():
    assert type(content.interactors_psicquic_resources()) == list


def test_interactors_static_acc():
    assert type(content.interactors_static_acc()) == dict


def test_interactors_acc_pathways():
    assert type(content.interactors_acc_pathways()) == list


def test_interactors_static_accs():
    assert type(content.interactors_static_accs()) == dict


def test_mapping():
    assert type(content.mapping()) == list


def test_orthology_events():
    assert type(content.orthology_events()) == dict


def test_orthology():
    assert type(content.orthology()) == dict


def test_participants():
    assert type(content.participants()) == list


def test_participants_physical_entities():
    assert type(content.participants_physical_entities()) == list


def test_participants_reference_entities():
    assert type(content.participants_reference_entities()) == list


def test_pathway_contained_event():
    assert type(content.pathway_contained_event()) == list


def test_pathway_contained_event_atttibute():
    assert type(content.pathway_contained_event_attribute()) == list


def test_pathways_low_diagram():
    assert type(content.pathways_low_diagram()) == list


def test_pathways_low_entity():
    assert type(content.pathways_low_entity()) == list


def test_pathways_top_level():
    assert type(content.pathways_top_level()) == list


def test_person_name():
    assert type(content.person_name()) == list


def test_person_id():
    assert type(content.person_id()) == dict


def test_query_id():
    assert type(content.query_id()) == dict


def test_query_ids():
    assert type(content.query_ids()) == list


def test_references():
    assert type(content.references()) == list


def test_species():
    assert type(content.species()) == list


def test_schema():
    assert type(content.schema(by=None)) == list
    assert type(content.schema(by="count")) == int
    assert type(content.schema(by="min")) == list
    assert type(content.schema(by="reference", name="ReferenceMolecule")) == list


def test_search_diagram():
    assert type(content.search_diagram()) == dict


def test_search_diagram_instance():
    assert type(content.search_diagram_instance()) == dict


def test_search_diagram_pathway_flag():
    assert type(content.search_diagram_pathway_flag()) == dict


def test_search_facet_query():
    assert type(content.search_facet_query()) == dict


def test_search_fireworks():
    assert type(content.search_fireworks()) == dict


def test_search_fireworks_flag():
    assert type(content.search_fireworks()) == dict


def test_search_query():
    assert type(content.search_query()) == dict


def test_search_spellcheck():
    assert type(content.search_spellcheck()) == list


def test_search_suggest():
    assert type(content.search_suggest()) == list
