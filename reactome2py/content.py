"""
Content Service for Reactome knowledgebase.
API calls are avaialble @ https://reactome.org/ContentService/#/   \n
Data model key classes for id query are available @ https://reactome.org/documentation/data-model
"""
from requests.exceptions import ConnectionError
import requests


NumberTypes = (int, float, complex)


def discover(id='R-HSA-446203'):
    """
    For each event (reaction or pathway) this method generates a json representing the dataset object as defined
    by schema.org (http). This is mainly used by search engines in order to index the data

    :param id: An event identifier ex. pathway stable identifier (stId) of pathway
    :return: Json dictionary object of The schema.org for an Event in Reactome knowledgebase
    """

    headers = {
        'accept': 'application/json',
    }

    url = 'https://reactome.org/ContentService/data/discover/%s' % id

    try:
        response = requests.get(url=url, headers=headers)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print('Status code returned a value of %s' % response.status_code)


def disease(doid=False):
    """
    Query list of diseases

    1. if doid is set to False
        * it retrieves the list of diseases annotated in Reactome

    2. if doid is set to True
        * it retrieves the list of disease DOIDs annotated in Reactome

    :param doid: Boolean param, if set to true - function returns a list of disease DOID
    :return: Json list object of diseases or disease DOID(s)
    """

    headers = {
        'accept': 'application/json',
    }

    if doid:
        url = 'https://reactome.org/ContentService/data/diseases/doid'
    else:
        url = 'https://reactome.org/ContentService/data/diseases'

    try:
        response = requests.get(url=url, headers=headers)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print('Status code returned a value of %s' % response.status_code)


def entities_complex(id='R-HSA-5674003', exclude_structures=False):
    """
    Retrieves the list of subunits that constitute any given complex.
    In case the complex comprises other complexes, this method recursively traverses the content returning each
    contained PhysicalEntity. Contained complexes and entity sets can be excluded setting the ‘exclude_structures’
    optional parameter to ‘true’

    :param id: The complex for which subunits are requested
    :param exclude_structures: Specifies whether contained complexes and entity sets are excluded in the response
    :return: Json list object with the entities contained in a given complex
    """

    if exclude_structures:
        exclude_structures = 'true'
    else:
        exclude_structures = 'false'

    headers = {
        'accept': 'application/json',
    }

    params = (
        ('excludeStructures', exclude_structures),
    )

    url = 'https://reactome.org/ContentService/data/complex/%s/subunits' % id

    try:
        response = requests.get(url=url, headers=headers, params=params)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print('Status code returned a value of %s' % response.status_code)


def entities_complexes(id='P00533', resource='UniProt'):
    """
    Retrieves the list of complexes that contain a given (identifier, resource). The method deconstructs the complexes
    into all its participants to do so.

    :param id: The resource's identifier for which complexes are requested
    :param resource: The resource of the identifier for complexes are requested
    :return: Json list object of complexes containing the pair (identifier, resource)
    """

    headers = {
        'accept': 'application/json',
    }

    url = 'https://reactome.org/ContentService/data/complexes/%s/%s' % (resource, id)

    try:
        response = requests.get(url=url, headers=headers)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print('Status code returned a value of %s' % response.status_code)


def entity_structures(id='R-HSA-199420'):
    """
    Retrieves the list of structures (Complexes and Sets) that include the given entity as their component.
    It should be mentioned that the list includes only simplified entries (type, names, ids) and not full information
    about each item.

    :param id: stable Identifier (stID) of a PhysicalEntity ex. PTEN [cytosol] R-HSA-199420'
    :return: Json list object of larger structures containing the entity
    """

    headers = {
        'accept': 'application/json',
    }

    url = 'https://reactome.org/ContentService/data/entity/%s/componentOf' % id

    try:
        response = requests.get(url=url, headers=headers)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print('Status code returned a value of %s' % response.status_code)


def entity_other_form(id='R-HSA-199420'):
    """
    Retrieves a list containing all other forms of the given PhysicalEntity.
    These other forms are PhysicalEntities that share the same ReferenceEntity identifier,
    ex. PTEN H93R[R-HSA-2318524] and PTEN C124R[R-HSA-2317439] are two forms of PTEN.

    :param id: dbId or stId of a PhysicalEntity
    :return: Json list object
    """

    headers = {
        'accept': 'application/json',
    }

    url = 'https://reactome.org/ContentService/data/entity/%s/otherForms' % id

    try:
        response = requests.get(url=url, headers=headers)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print('Status code returned a value of %s' % response.status_code)


def event_ancestors(id='R-HSA-5673001'):
    """
    The Reactome definition of events includes pathways and reactions.
    Although events are organised in a hierarchical structure, a single event can be in more than one location,
    i.e. a reaction can take part in different pathways while, in the same way, a sub-pathway can take part
    in many pathways. Therefore, this method retrieves a list of all possible paths from the requested event to the
    top level pathway(s).

    :param id: The event for which the ancestors are requested
    :return: Json list object of the ancestors of a given event
    """

    headers = {
        'accept': 'application/json',
    }

    url = 'https://reactome.org/ContentService/data/event/%s/ancestors' % id

    try:
        response = requests.get(url=url, headers=headers)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print('Status code returned a value of %s' % response.status_code)


def event_species(species='9606'):
    """
    Events (pathways and reactions) in Reactome are organised in a hierarchical structure for every species.
    By following all ‘hasEvent’ relationships, this method retrieves the full event hierarchy for any given species.
    The result is a list of tree structures, one for each TopLevelPathway. Every event in these trees is represented
    by a PathwayBrowserNode. The latter contains the stable identifier, the name, the species, the url, the type, and
    the diagram of the particular event.

    :param species: Species name (ex: Homo sapiens) or species taxId (ex: 9606)
    :return: Json list object of the full event hierarchy for a given species
    """
    headers = {
        'accept': 'application/json',
    }

    url = 'https://reactome.org/ContentService/data/eventsHierarchy/%s' % species

    try:
        response = requests.get(url=url, headers=headers)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print('Status code returned a value of %s' % response.status_code)


def export_diagram(id='R-HSA-177929', ext='png', quality='5', flag_interactors=False, title=True, margin='15',
                   ehld=True, diagram_profile='Modern', resource='Total', analysis_profile='Standard', token=None,
                   flag=None, sel=[], exp_column=None, file='report', path=''):
    """
    This method accepts identifiers for Event class instances.
        * When a diagrammed pathway is provided, the diagram is exported to the specified format.
        * When a subpathway is provided, the diagram for the parent is exported and the events that are part of the subpathways are selected.
        * When a reaction is provided, the diagram containing the reaction is exported and the reaction is selected.

    :param id: Event identifier (it can be a pathway with diagram, a subpathway or a reaction)
    :param ext: File extension (defines the image format) available extensions: png, jpg, jpeg, svg, gif
    :param quality: Result image quality between [1 - 10]. It defines the quality of the final image (Default 5)
    :param flag: Gene name, protein or chemical identifier or Reactome identifier used to flag elements in the diagram
    :param flag_interactors: Defines whether to take into account interactors for the flagging default set to False
    :param sel: Highlight element(s) selection in the diagram. CSV line. comma seperate python list ex ['X', 'Y', 'Z']
    :param token: The analysis token with the results to be overlaid on top of the given diagram
    :param title: Sets whether the name of the pathway is shown as title
    :param margin: Defines the image margin between [0 - 20] (Default 15)
    :param ehld: Defines whether textbook-like illustration are taken into account
    :param diagram_profile: Diagram Color Profile: Modern or Standard
    :param resource: The analysis resource for which the results will be overlaid on top of the given pathways overview
    :param exp_column: Expression column. When the token is associated to an expression analysis, this parameter allows specifying the expression column for the overlay
    :param analysis_profile: Analysis Color Profile: Standard, Strosobar, Copper Plus
    :param file: Name of file default is 'report'
    :param path: Absolute path to save the file to
    :return: Exports a given pathway diagram to the specified image format (png, jpg, jpeg, svg, gif)
    """

    if flag_interactors:
        flag_interactors = 'true'
    else:
        flag_interactors = 'false'

    if title:
        title = 'true'
    else:
        title = 'false'

    if ehld:
        ehld = 'true'
    else:
        ehld = 'false'

    headers = {
        'accept': 'image/png',
    }

    params = (
        ('token', token),
        ('flg', flag),
        ('sel', sel),
        ('expColumn', exp_column),
        ('quality', quality),
        ('flgInteractors', flag_interactors),
        ('title', title),
        ('margin', margin),
        ('ehld', ehld),
        ('diagramProfile', diagram_profile),
        ('resource', resource),
        ('analysisProfile', analysis_profile),
    )

    url = ".".join(['https://reactome.org/ContentService/exporter/diagram/%s' % id, ext])

    path = "".join([path, ".".join([file, ext])])

    try:
        response = requests.get(url=url, headers=headers, params=params)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        with open(path, 'wb') as f:
            for chunk in response:
                f.write(chunk)
    else:
        print('Status code returned a value of %s' % response.status_code)


def export_document(id='R-HSA-177929', level='1', diagram_profile='Modern', resource='Total',
                    analysis_profile='Standard', token=None, exp_column=None, file='report', path=''):
    """
    This method accepts identifiers for Event class instances.
    The generated document contains the details for the given event and, optionally, its children (see level parameter).

    These details include:
        * A diagram image
        * Summation
        * Literature references
        * Edit history
        * Other details: type, location, compartments, diseases

    Documents can also be overlaid with pathway analysis results (given a token)

    :param id: Event identifier (it can be a pathway with diagram, a subpathway or a reaction)
    :param level: Number of levels to explore down in the pathways hierarchy [0 - 1]
    :param diagram_profile: Diagram Color Profile Modern or Standard
    :param resource: The analysis resource for which the results will be overlaid on top of the given pathways overview
    :param analysis_profile: Analysis Color Profile: Standard, Strosobar, Copper Plus
    :param token: The analysis token with the results to be overlaid on top of the given diagram
    :param exp_column: Expression column. When the token is associated to an expression analysis, this parameter allows specifying the expression column for the overlay
    :param file: Name of file default is 'report'
    :param path: Absolute path to save the file to
    :return: Exports the content of a given event (pathway or reaction) to a PDF document
    """

    headers = {
        'accept': 'application/pdf',
    }

    params = (
        ('token', token),
        ('expColumn', exp_column),
        ('level [0 - 1]', level),
        ('diagramProfile', diagram_profile),
        ('resource', resource),
        ('analysisProfile', analysis_profile),
    )

    url = 'https://reactome.org/ContentService/exporter/document/event/%s.pdf' % id

    path = "".join([path, ".".join([file, 'pdf'])])

    try:
        response = requests.get(url=url, headers=headers, params=params)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        with open(path, 'wb') as f:
            for chunk in response:
                f.write(chunk)
    else:
        print('Status code returned a value of %s' % response.status_code)


def export_event(id='R-HSA-177929', format='sbgn', file='report', path=''):
    """
    Exports a given pathway or reaction to the format requested:
        * Systems Biology Graphical Notation (SBGN)
        * Systems Biology Markup Language (SBML)

    :param id: DbId or StId of the requested pathway or reaction
    :param format: sbgn or sbml
    :param file: Name of file default is set to report
    :param path: Absolute path to save the file
    :return: Exports a given pathway or reaction to SBGN
    """

    headers = {
        'accept': '*/*',
    }

    if format in 'sbml':
        ext = 'sbml'
    if format in 'sbgn':
        ext = 'sbgn'

    url = ".".join(['https://reactome.org/ContentService/exporter/event/%s' % id, ext])

    path = "".join([path, ".".join([file, ext])])

    try:
        response = requests.get(url=url, headers=headers)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        with open(path, 'wb') as f:
            for chunk in response:
                f.write(chunk)
    else:
        print('Status code returned a value of %s' % response.status_code)


def export_fireworks(species='9606', ext='png', file='report', path='', quality='5', flag=None, flag_interactors=False,
                     sel=[], title=True, margin='15', resource='Total', diagram_profile='', coverage=False, token=None,
                     exp_column=None):
    """
    Exports a given pathway overview to the specified image format (png, jpg, jpeg, svg, gif)
    https://reactome.org/dev/pathways-overview/js


    :param species: Species identifier (it can be the taxonomy id, species name or dbId)
    :param ext: File extension (defines the image format) available extensions: png, jpg, jpeg, svg, gif
    :param file: Name of file default is set to report
    :param path: Absolute path to save the file
    :param quality: Result image quality between [1 - 10]. It defines the quality of the final image (Default 5)
    :param flag: Gene name, protein or chemical identifier or Reactome identifier used to flag elements in the diagram
    :param flag_interactors: Defines whether to take into account interactors for the flagging
    :param sel: Highlight element(s) selection in the diagram. CSV line. comma seperate python list ex ['X', 'Y', 'Z']
    :param title: Sets whether the name of the pathway is shown below
    :param margin: Defines the image margin between [0 - 20] (Default 15)
    :param resource: The analysis resource for which the results will be overlaid on top of the given pathways overview
    :param diagram_profile: Diagram Color Profile available in: Copper, Copper plus, Barium lithium, Calcium salts
    :param coverage: Set to ‘true’ to overlay analysis coverage values default is set to false
    :param token: The analysis token with the results to be overlaid on top of the given pathways overview
    :param exp_column: Expression column. When the token is associated to an expression analysis, this parameter allows specifying the expression column for the overlay
    :return: Exports a given pathway overview to the specified image format (png, jpg, jpeg, svg, gif)
    """

    if flag_interactors:
        flag_interactors = 'true'
    else:
        flag_interactors = 'false'

    if title:
        title = 'true'
    else:
        title = 'false'

    if coverage:
        coverage = 'true'
    else:
        coverage = 'false'

    headers = {
        'accept': 'image/png',
    }

    params = (
        ('quality', quality),
        ('flg', flag),
        ('flgInteractors', flag_interactors),
        ('sel', sel),
        ('title', title),
        ('margin', margin),
        ('diagramProfile', diagram_profile),
        ('resource', resource),
        ('coverage', coverage),
        ('token', token),
        ('expColumn', exp_column),
    )

    url = ".".join(['https://reactome.org/ContentService/exporter/fireworks/%s' % species, ext])

    path = "".join([path, ".".join([file, ext])])

    try:
        response = requests.get(url=url, headers=headers, params=params)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        with open(path, 'wb') as f:
            for chunk in response:
                f.write(chunk)
    else:
        print('Status code returned a value of %s' % response.status_code)


def export_reaction(id='R-HSA-6787403', ext='png', file='report', path='', quality='5', flag=None, flag_interactors=False,
                     sel=[], title=True, margin='15', resource='Total', diagram_profile='', coverage=False, token=None,
                     exp_column=None):
    """
    Exports a given reaction to the specified image format (png, jpg, jpeg, svg, gif)

    :param id: Reaction identifier
    :param ext: File extension (defines the image format) available extensions: png, jpg, jpeg, svg, gif
    :param file: Name of file default is set to report
    :param path: Absolute path to save the file
    :param quality: Result image quality between [1 - 10]. It defines the quality of the final image (Default 5)
    :param flag: Gene name, protein or chemical identifier or Reactome identifier used to flag elements in the diagram
    :param flag_interactors: Defines whether to take into account interactors for the flagging
    :param sel: Highlight element(s) selection in the diagram. CSV line. comma seperate python list ex ['X', 'Y', 'Z']
    :param title: Sets whether the name of the pathway is shown below
    :param margin: Defines the image margin between [0 - 20] (Default 15)
    :param resource: The analysis resource for which the results will be overlaid on top of the given pathways overview
    :param diagram_profile: Diagram Color Profile available in: Copper, Copper plus, Barium lithium, Calcium salts
    :param coverage: Set to ‘true’ to overlay analysis coverage values default is set to false
    :param token: The analysis token with the results to be overlaid on top of the given pathways overview
    :param exp_column: Expression column. When the token is associated to an expression analysis, this parameter allows specifying the expression column for the overlay
    :return:
    """

    if flag_interactors:
        flag_interactors = 'true'
    else:
        flag_interactors = 'false'

    if title:
        title = 'true'
    else:
        title = 'false'

    if coverage:
        coverage = 'true'
    else:
        coverage = 'false'

    headers = {
        'accept': 'image/png',
    }

    params = (
        ('quality', quality),
        ('flg', flag),
        ('flgInteractors', flag_interactors),
        ('sel', sel),
        ('title', title),
        ('margin', margin),
        ('diagramProfile', diagram_profile),
        ('resource', resource),
        ('coverage', coverage),
        ('token', token),
        ('expColumn', exp_column),
    )

    url = ".".join(['https://reactome.org/ContentService/exporter/reaction/%s' % id, ext])

    path = "".join([path, ".".join([file, ext])])

    try:
        response = requests.get(url=url, headers=headers, params=params)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        with open(path, 'wb') as f:
            for chunk in response:
                f.write(chunk)
    else:
        print('Status code returned a value of %s' % response.status_code)


def interactors_psicquic_acc(resource='MINT', acc='Q13501', by='details'):
    """
    1. if by details
        * Retrieve clustered interaction, sorted by score, of a given accession by resource
    2. if by summary
        * Retrieve a summary of a given accession by resource

    :param resource: Proteomics standards initiative common query interface (PSICQUIC) Resource
        use interactors_psicquic_resources to retrive all active resources
    :param acc: Single Accession
    :param by: details or summary (returns counts of details available)
    :return: Json dictionary object
    """

    headers = {
        'accept': 'application/json',
    }

    if by in 'details':
        url = 'https://reactome.org/ContentService/interactors/psicquic/molecule/%s/%s/details' % (resource, acc)
    if by in 'summary':
        url = 'https://reactome.org/ContentService/interactors/psicquic/molecule/%s/%s/summary' % (resource, acc)

    try:
        response = requests.get(url=url, headers=headers)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print('Status code returned a value of %s' % response.status_code)


def interactors_psicquic_accs(proteins='EGFR', resource='MINT', by='details'):
    """
    1. if by details
        * Retrieve clustered interaction, sorted by score, of a given accession(s) by resource.
    2. if by summary
        * Retrieve a summary of a given accession list by resource.

    :param proteins: Comma seperate list of Accessions in string format 'a1,a2,a3'
    :param resource: Proteomics standards initiative common query interface (PSICQUIC) Resource
        use interactors_psicquic_resources to retrive all active resources
    :return: Json dictionary object
    """

    headers = {
        'accept': 'application/json',
        'content-type': 'text/plain',
    }

    data = proteins

    if by in 'details':
        url = 'https://reactome.org/ContentService/interactors/psicquic/molecules/%s/details' % resource
    if by in 'summary':
        url = 'https://reactome.org/ContentService/interactors/psicquic/molecules/%s/summary' % resource

    try:
        response = requests.post(url=url, headers=headers, data=data)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print('Status code returned a value of %s' % response.status_code)


def interactors_psicquic_resources():
    """
    Retrieve a list of all Psicquic Registries services

    :return: Json list object
    """

    headers = {
        'accept': 'application/json',
    }

    url = 'https://reactome.org/ContentService/interactors/psicquic/resources'

    try:
        response = requests.get(url=url, headers=headers)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print('Status code returned a value of %s' % response.status_code)


def interactors_static_acc(acc='Q13501', page='-1', page_size='-1', by='details'):
    """
    1. if by details:
        * retrieve a detailed interaction information of a given accession
    2. if by summary:
        * retrieve a summary of a given accession

    :param acc: Interactor accession (or identifier)
    :param page: For paginating the results
    :param page_size: Number of results to be retrieved
    :param by: details or summary (returns counts of details available)
    :return: Json dictionary object
    """

    if isinstance(page_size, NumberTypes):
        page_size = str(page_size)

    if isinstance(page, NumberTypes):
        page = str(page)

    headers = {
        'accept': 'application/json',
    }

    params = (
        ('page', page),
        ('pageSize', page_size),
    )

    if by in 'details':
        url = 'https://reactome.org/ContentService/interactors/static/molecule/%s/details' % acc
    if by in 'summary':
        url = 'https://reactome.org/ContentService/interactors/static/molecule/%s/summary' % acc

    try:
        response = requests.get(url=url, headers=headers, params=params)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print('Status code returned a value of %s' % response.status_code)


def interactors_acc_pathways(acc='Q9BXM7-1', species='Homo sapiens', only_diagrammed=False):
    """
    Retrieve a list of lower level pathways where the interacting molecules can be found

    :param acc: Accession
    :param species: The species name for which the pathways are requested (e.g. ‘Homo sapiens’)
    :param only_diagrammed: Specifies whether the pathways has to have an associated diagram or not
    :return: Json list object
    """

    headers = {
        'accept': 'application/json',
    }

    params = (
        ('species', species),
        ('onlyDiagrammed', only_diagrammed),
    )

    url = 'https://reactome.org/ContentService/interactors/static/molecule/%s/pathways' % acc

    try:
        response = requests.get(url=url, headers=headers, params=params)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print('Status code returned a value of %s' % response.status_code)


def interactors_static_accs(accs='Q9BXM7-1', by='details', page='-1', page_size='-1'):
    """
    1. if by details:
        * Retrieve clustered interaction, sorted by score, of a given accession(s) by resource.
    2. if by summary:
        * Retrieve a summary of a given accession list by resource.

    :param accs: Comma seperate list of Accessions in string format 'a1,a2,a3'
    :param by: details or summary (returns counts of details available)
    :param page: For paginating the results
    :param page_size: Number of results to be retrieved
    :return: Json dictionary object
    """

    if isinstance(page_size, NumberTypes):
        page_size = str(page_size)

    if isinstance(page, NumberTypes):
        page = str(page)

    headers = {
        'accept': 'application/json',
        'content-type': 'text/plain',
    }

    data = accs

    if by in 'details':
        url = 'https://reactome.org/ContentService/interactors/static/molecules/details'
        params = (
            ('page', page),
            ('pageSize', page_size),
        )

    if by in 'summary':
        url = 'https://reactome.org/ContentService/interactors/static/molecules/summary'
        params = None

    try:
        response = requests.post(url=url, headers=headers, params=params, data=data)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print('Status code returned a value of %s' % response.status_code)


def token_interactors(token, proteins):
    """
    Retrieve custom interactions associated with a token

    :param token: A token associated with a data submission
    :param proteins: Interactors accessions
    :return:  Retrieve custom interactions associated with a token
    """

    headers = {
        'accept': 'application/json',
        'content-type': 'text/plain',
    }

    data = proteins

    url = 'https://reactome.org/ContentService/interactors/token/%s' % token

    try:
        response = requests.post(url=url, headers=headers, data=data)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print('Status code returned a value of %s' % response.status_code)


def interactors_psicquic_url(name, psicquic_url):
    """
    Registry custom PSICQUIC resource

    :param name: Name which identifies the custom psicquic
    :param psicquic_url: A URL pointing to the Custom PSICQUIC Resource
    :return: Registry custom PSICQUIC resource
    """

    headers = {
        'accept': 'application/json',
        'content-type': 'text/plain',
    }

    params = (
        ('name', name),
    )

    data = psicquic_url

    url = 'https://reactome.org/ContentService/interactors/upload/psicquic/url'

    try:
        response = requests.post(url=url, headers=headers, params=params, data=data)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print('Status code returned a value of %s' % response.status_code)


def interactors_upload_content(name, content):
    """
    Paste file content and get a summary associated with a token

    :param name: Name which identifies the sample
    :param content: Paste custom interactors file content
    :return: Paste file content and get a summary associated with a token
    """

    headers = {
        'accept': 'application/json',
        'content-type': 'text/plain',
    }

    params = (
        ('name', name),
    )

    data = content

    url = 'https://reactome.org/ContentService/interactors/upload/tuple/content'

    try:
        response = requests.post(url=url, headers=headers, params=params, data=data)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print('Status code returned a value of %s' % response.status_code)


def interactors_form(path, name):
    """
    Parse file and retrieve a summary associated with a token

    :param path: Absolute path to file to be read with custom interactor
    :param name: Name which identifies the sample
    :return: 
    """

    headers = {
        'accept': 'application/json',
        'content-type': 'text/plain',
    }

    params = (
        ('name', name),
    )

    url = 'https://reactome.org/ContentService/interactors/upload/tuple/form'

    data = open(path, 'rb').read()

    try:
        response = requests.post(url=url, headers=headers, params=params, data=data)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print('Status code returned a value of %s' % response.status_code)


def interactors_url(name, interactors_url):
    """
    Send file via URL and get a summary associated with a token

    :param name: Name which identifies the sample
    :param interactors_url: A URL pointing to the Interactors file
    :return:
    """

    headers = {
        'accept': 'application/json',
        'content-type': 'text/plain',
    }

    params = (
        ('name', name),
    )

    url = 'https://reactome.org/ContentService/interactors/upload/tuple/url'

    data = interactors_url

    try:
        response = requests.post(url=url, headers=headers, params=params, data=data)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print('Status code returned a value of %s' % response.status_code)


def mapping(id='PTEN', resource='UniProt', species='9606', by='pathways'):
    """
    1. by pathways:
        Entities play different roles in reactions, and reactions are events that conform a pathway. This method retrieves
        the pathways for which an identifier plays a role within one or more of their events.
        return: The lower level pathways where an identifier can be mapped to

    2. by reactions:
        Entities play different roles in reactions. This method retrieves the reactions for which an identifier plays a role .
        return: The reactions where an identifier can be mapped to

    :param id: The identifier to be mapped
    :param resource: The resource name for which the identifier is submitted
    :param species: Species for which the result is filtered. Accepts taxonomy id, species name and dbId.
        Important Note - when identifier points to chemical, this becomes mandatory and if not provided, the default is ‘Homo sapiens’
    :param by: pathways or reactions
    :return: Json list object
    """

    headers = {
        'accept': 'application/json',
    }

    params = (
        ('species', species),
    )

    if by in 'pathways':
        url = 'https://reactome.org/ContentService/data/mapping/%s/%s/pathways' % (resource, id)
    if by in 'reactions':
        url = 'https://reactome.org/ContentService/data/mapping/%s/%s/reactions' % (resource, id)

    try:
        response = requests.get(url=url, headers=headers, params=params)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print('Status code returned a value of %s' % response.status_code)


def orthology_events(ids='R-HSA-6799198,R-HSA-168256,R-HSA-168249', species='49633'):
    """
    Reactome uses the set of manually curated human reactions to computationally infer reactions in
    twenty evolutionarily divergent eukaryotic species for which high-quality whole-genome sequence
    data are available, and hence a comprehensive and high-quality set of protein predictions exists.
    Thus, this method retrieves the orthologies for any given set of events or entities in the specified species.

    :param ids: The events identifiers for which the orthology is requested
    :param species: The species id for which the orthology is requested
    :return: Json dictionary object of the orthologies of a given set of events or entities
    """

    headers = {
        'accept': 'application/json',
        'content-type': 'text/plain',
    }

    data = ids

    url = 'https://reactome.org/ContentService/data/orthologies/ids/species/%s' % species

    try:
        response = requests.post(url=url, headers=headers, data=data)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print('Status code returned a value of %s' % response.status_code)


def orthology(id='R-HSA-6799198', species='49633'):
    """
    Reactome uses the set of manually curated human reactions to computationally infer reactions in
    twenty evolutionarily divergent eukaryotic species for which high-quality whole-genome sequence data
    are available, and hence a comprehensive and high-quality set of protein predictions exists.
    Thus, this method retrieves the orthology for any given event or entity in the specified species.

    :param id: The event for which the orthology is requested
    :param species: The species id for which the orthology is requested
    :return: Json dictionary object of the orthology for a given event or entity
    """

    headers = {
        'accept': 'application/json',
        'content-type': 'text/plain',
    }

    url = 'https://reactome.org/ContentService/data/orthology/%s/species/%s' % (id, species)

    try:
        response = requests.get(url=url, headers=headers)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print('Status code returned a value of %s' % response.status_code)


def participants(id='5205685'):
    """
    Participants contains a PhysicalEntity (dbId, displayName) and a collection of ReferenceEntities (dbId, name, identifier, url)

    :param id: dbId or stId of a PhysicalEntity
    :return: Json list obj of participants for a given event
    """

    headers = {
        'accept': 'application/json',
    }

    url = 'https://reactome.org/ContentService/data/participants/%s' % id

    try:
        response = requests.get(url=url, headers=headers)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print('Status code returned a value of %s' % response.status_code)


def participants_physical_entities(id='R-HSA-5205685'):
    """
    This method retrieves all the PhysicalEntities that take part in a given event. It is worth mentioning that
    because a pathway can contain smaller pathways (subpathways), the method also recursively retrieves the
    PhysicalEntities from every constituent

    :param id: The event for which the participating PhysicalEntities are requested
    :return: Json list object of participating PhysicalEntities for a given event
    """

    headers = {
        'accept': 'application/json',
    }

    url = 'https://reactome.org/ContentService/data/participants/%s/participatingPhysicalEntities' % id

    try:
        response = requests.get(url=url, headers=headers)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print('Status code returned a value of %s' % response.status_code)


def participants_reference_entities(id='5205685'):
    """
    PhysicalEntity instances that represent, e.g., the same chemical in different compartments, or different
    post-translationally modified forms of a single protein, share numerous invariant features such as names,
    molecular structure and links to external databases like UniProt or ChEBI. To enable storage of this shared
    information in a single place, and to create an explicit link among all the variant forms of what can also be
    seen as a single chemical entity, Reactome creates instances of the separate ReferenceEntity class.
    A ReferenceEntity instance captures the invariant features of a molecule. This method retrieves the
    ReferenceEntities of all PhysicalEntities that take part in a given event. It is worth mentioning that
    because a pathway can contain smaller pathways (subpathways), this method also recursively retrieves the
    ReferenceEntities for all PhysicalEntities in every constituent pathway.

    :param id: The event for which the participating ReferenceEntities are requested
    :return: Json list object of participating ReferenceEntities for a given event
    """

    headers = {
        'accept': 'application/json',
    }

    url = 'https://reactome.org/ContentService/data/participants/%s/referenceEntities' % id

    try:
        response = requests.get(url=url, headers=headers)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print('Status code returned a value of %s' % response.status_code)


def pathway_contained_event(id='R-HSA-5673001'):
    """
    Events are the building blocks used in Reactome to represent all biological processes,
    and they include pathways and reactions. Typically, an event can contain other events. For example,
    a pathway can contain smaller pathways and reactions. This method recursively retrieves all the events
    contained in any given event.

    :param id: The event for which the contained events are requested
    :return: Json list object of all the events contained in the given event
    """

    headers = {
        'accept': 'application/json',
    }

    url = 'https://reactome.org/ContentService/data/pathway/%s/containedEvents' % id

    try:
        response = requests.get(url=url, headers=headers)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print('Status code returned a value of %s' % response.status_code)


def pathway_contained_event_atttibute(id='R-HSA-5673001', attribute='stId'):
    """
    Events are the building blocks used in Reactome to represent all biological processes, and they
    include pathways and reactions. Typically, an event can contain other events. For example, a pathway
    can contain smaller pathways (subpathways) and reactions. This method recursively retrieves a single attribute for
    each of the events contained in the given event.

    :param id: The event for which the contained events are requested
    :param attribute: Attribute to be filtered
    :return: List object of a single property for each event contained in the given event
    """

    headers = {
        'accept': 'text/plain',
    }

    url = 'https://reactome.org/ContentService/data/pathway/%s/containedEvents/%s' % (id, attribute)

    try:
        response = requests.get(url=url, headers=headers)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.text.strip('][').split(', ')
    else:
        print('Status code returned a value of %s' % response.status_code)


def pathways_low_diagram(id='R-HSA-199420', species=None, all_forms=False):
    """
    This method traverses the event hierarchy and retrieves the list of all lower level pathways that have a
    diagram and contain the given PhysicalEntity or Event.

    * if all_forms is set to true: it retrieves the given PhysicalEntity in any of its variant forms. These variant forms include for example different post-translationally modified versions of a single protein, or the same chemical in different compartments.

    :param id: The entity that has to be present in the pathways
    :param species: The species for which the pathways are requested. Taxonomy identifier (eg: 9606) or species name (eg: ‘Homo sapiens’)
    :param all_forms: If true, it retrieves the given PhysicalEntity in any of its variant forms.
    :return: Json list object of lower level pathways with diagram containing a given entity or event
    """

    headers = {
        'accept': 'application/json',
    }

    params = (
        ('species', species),
    )

    if all_forms:
        url = 'https://reactome.org/ContentService/data/pathways/low/diagram/entity/%s/allForms' % id
    else:
        url = 'https://reactome.org/ContentService/data/pathways/low/diagram/entity/%s' % id

    try:
        response = requests.get(url=url, headers=headers, params=params)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print('Status code returned a value of %s' % response.status_code)


def pathways_low_entity(id='R-HSA-199420', species=None, all_forms=False):
    """
    This method traverses the event hierarchy and retrieves the list of all lower level pathways that contain
    the given PhysicalEntity or Event.

    * if all_forms is set to true, it retrieves the list of all lower level pathways that contain the given PhysicalEntity in any of its variant forms. These variant forms include for example different post-translationally modified versions of a single protein, or the same chemical in different compartments.

    :param id: The entity that has to be present in the pathways
    :param species: The species for which the pathways are requested. Taxonomy identifier (eg: 9606) or species name (eg: ‘Homo sapiens’)
    :param all_forms: If set to true, it retrieves the list of all lower level pathways that contain the given PhysicalEntity in any of its variant forms.
    :return: Json list object of lower level pathways containing a given entity or event
    """

    headers = {
        'accept': 'application/json',
    }

    params = (
        ('species', species),
    )

    if all_forms:
        url = 'https://reactome.org/ContentService/data/pathways/low/entity/%s' % id
    else:
        url = 'https://reactome.org/ContentService/data/pathways/low/entity/%s/allForms' % id

    try:
        response = requests.get(url=url, headers=headers, params=params)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print('Status code returned a value of %s' % response.status_code)


def pathways_top_level(species='9606'):
    """
    This method retrieves the list of top level pathways for the given species

    :param species: Specifies the species by the taxonomy identifier (eg: 9606) or species name (eg: ‘Homo+sapiens’)
    :return: Json list object of all Reactome top level pathways
    """

    headers = {
        'accept': 'application/json',
    }

    url = 'https://reactome.org/ContentService/data/pathways/top/%s' % species

    try:
        response = requests.get(url=url, headers=headers)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print('Status code returned a value of %s' % response.status_code)


def person_name(name='Steve Jupe', exact=False):
    """
    Retrieves a list of people in Reactome with either their first or last name partly matching the given name (string).

    * If exact is set to true, retrieves a list of people in Reactome with either their first or last name matching exactly the given name (string).

    :param name: Person’s first or last name
    :param exact:
    :return: Json list object of people with first or last name partly or exactly matching a given name (string)
    """

    headers = {
        'accept': 'application/json',
    }

    if exact:
        url = 'https://reactome.org/ContentService/data/people/name/%s/exact' % name
    else:
        url = 'https://reactome.org/ContentService/data/people/name/%s' % name

    try:
        response = requests.get(url=url, headers=headers)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print('Status code returned a value of %s' % response.status_code)


def person_id(id='0000-0001-5807-0069', by=None, attribute=None):
    """
    1. With only id parameter declared,
        * Retrieves a person in Reactome by his/her OrcidId or DbId.

    2. With id and query by declared with pathway or publication
        * Retrieves a list of pathways authored by a given person. OrcidId, DbId or Email can be used to specify the person.
        * Retrieves a list of publications authored by a given person. OrcidId, DbId or Email can be used to specify the person.

    3. With id and attribute declared
        * Retrieves a specific person’s property by his/her OrcidId or DbId.

    :param id: Person identifier - Can be OrcidId or DbId
    :param by: if not None, query by authored: pathways or publications
    :param attribute: Attribute to be filtered ex. displayName
    :return: Json dictionary object
    """

    headers = {
        'accept': 'application/json',
    }

    if id and by is None and attribute is None:
        url = 'https://reactome.org/ContentService/data/person/%s' % id

    if id and by and attribute is None:
        by = by.lower()
        if by in 'publication':
            url = 'https://reactome.org/ContentService/data/person/%s/publications' % id
        if by in 'pathway':
            url = 'https://reactome.org/ContentService/data/person/%s/authoredPathways' % id

    if id and attribute:
        url = 'https://reactome.org/ContentService/data/person/%s/%s' % (id, attribute)

    try:
        response = requests.get(url=url, headers=headers)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print('Status code returned a value of %s' % response.status_code)


def query_id(id='R-HSA-60140', enhanced=False, attribute=None):
    """
    This method queries for an entry in Reactome knowledgebase based on the given identifier, i.e. stable id or
    database id. It is worth mentioning that the retrieved database object has all its properties and direct
    relationships (relationships of depth 1) filled.

    * if enhanced is set to true it also includes any second level relationships regarding regulations and catalysts.
    * if attribute name is present it queries the property of the attribute requested

    :param id: DbId or StId of the requested database object
    :param enhanced: boolean value to make an enhanced query on id
    :param attribute: Attribute to be queried
    :return: Json dictionary object
    """

    headers = {
        'accept': 'application/json',
    }

    if id and enhanced is False and attribute is None:
        url = 'https://reactome.org/ContentService/data/query/%s' % id

    if id and enhanced:
        url = 'https://reactome.org/ContentService/data/query/enhanced/%s' % id

    if id and attribute:
        url = 'https://reactome.org/ContentService/data/query/%s/%s' % (id, attribute)

    try:
        response = requests.get(url=url, headers=headers)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print('Status code returned a value of %s' % response.status_code)


def query_ids(ids='R-HSA-60140', mapping=False):
    """
    This method queries for a set of entries in Reactome knowledgebase based on the given list of identifiers.
    The provided list of identifiers can include stable ids, database ids or a mixture of both. It should be
    underlined that any duplicated ids are eliminated while only requests containing up to 20 ids are processed.

    * if mapping is set, to true previous version of stable identifiers can be queried.

    :param ids: A comma separated list of identifiers
    :param mapping: If set to true, retrieves a list of entries with their mapping to the provided identifiers
    :return: Json list object
    """

    headers = {
        'accept': 'application/json',
        'content-type': 'text/plain',
    }

    data = ids

    if mapping:
        url = 'https://reactome.org/ContentService/data/query/ids/map'
    else:
        url = 'https://reactome.org/ContentService/data/query/ids'

    try:
        response = requests.post(url=url, headers=headers, data=data)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print('Status code returned a value of %s' % response.status_code)


def references(id='15377'):
    """
    Retrieves a list containing all the reference entities for a given identifier.

    :param id: Identifier for a given entity
    :return: Json list obkect of all ReferenceEntities for a given identifier
    """

    headers = {
        'accept': 'application/json',
    }

    url = 'https://reactome.org/ContentService/references/mapping/%s' % id

    try:
        response = requests.get(url=url, headers=headers)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print('Status code returned a value of %s' % response.status_code)


def species(by='all'):
    """
    Query species by:
        * all, returns list of all species in Reactome
        * main, return list of main species in Reactome

    :param by: all or main
    :return: Json list object
    """

    headers = {
        'accept': 'application/json',
    }

    by = by.lower()

    if by in 'all':
        url = 'https://reactome.org/ContentService/data/species/all'
    if by in 'main':
        url = 'https://reactome.org/ContentService/data/species/main'

    try:
        response = requests.get(url=url, headers=headers)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print('Status code returned a value of %s' % response.status_code)


def schema(name='Pathway', by='count', species='9606', page='-1', offset='20000'):
    """
    This method retrieves the list of entries in Reactome that belong to the specified schema class.
    Please take into account that if species is specified to filter the results, schema class needs to be an
    instance of Event or PhysicalEntity. Additionally, paging is required, while a maximum of 25 entries can be
    returned per request.

    1. if by is count:
        * counts the total number of entries in Reactome that belong to the specified schema class.
    2. if by is min:
        * the list of simplified entries in Reactome that belong to the specified schema class. A simplified entry may be considered as a minimised version of the full database object that includes its database id, stable id, displayName and type.
    3. if by is reference:
        * the list of simplified reference objects that belong to the specified schema class. A reference object includes its database id, external identifier, and external database name. ex. name='ReferenceMolecule'

    :param name: Schema class name.
    :param by: if not None, by count, min, or reference (name needs to an instance of ReferenceEntity or ExternalOntology)
    :param species: Allowed species filter: SpeciesName (eg: Homo sapiens) SpeciesTaxId (eg: 9606)
    :param offset: Number of rows returned. Maximum = 25
    :param page: Page to be returned
    :return: int if by = count, json list if by = min or reference
    """

    if isinstance(page, NumberTypes):
        page = str(page)

    if isinstance(offset, NumberTypes):
        offset = str(offset)

    headers = {
        'accept': 'application/json',
    }

    if by is None:
        url = 'https://reactome.org/ContentService/data/schema/%s' % name

        params = (
            ('species', species),
            ('page', page),
            ('offset', offset),
        )

    if by and by.lower() in 'count':
        url = 'https://reactome.org/ContentService/data/schema/%s/count' % name

        params = (
            ('species', species),
        )

    if by and by.lower() in 'min':
        url = 'https://reactome.org/ContentService/data/schema/%s/min' % name

        params = (
            ('species', species),
            ('page', page),
            ('offset', offset),
        )

    if by and by.lower() in 'reference':
        url = 'https://reactome.org/ContentService/data/schema/%s/reference' % name

        params = (
            ('page', page),
            ('offset', offset),
        )

    try:
        response = requests.get(url=url, headers=headers, params=params)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print('Status code returned a value of %s' % response.status_code)


def search_diagram(diagram='R-HSA-8848021', query='MAD', types=[], start=None, rows=None):
    """
    Performs a Apache Solr query (diagram widget scoped) for a given QueryObject

    :param diagram: diagram/pathway stable id
    :param query: query names by this string
    :param types: types to filter
    :param start: start row
    :param rows: number of rows to include
    :return: Json dictionary object
    """

    headers = {
        'accept': 'application/json',
    }

    params = (
        ('query', query),
        ('types', types),
        ('start', start),
        ('rows', rows),
    )

    url = 'https://reactome.org/ContentService/search/diagram/%s' % diagram

    try:
        response = requests.get(url=url, headers=headers, params=params)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print('Status code returned a value of %s' % response.status_code)


def search_diagram_instance(diagram='R-HSA-68886', instance='R-HSA-141433', types=[]):
    """
    Performs a Apache Solr query (diagram widget scoped) for a given QueryObject

    :param diagram: diagram/pathway stable id
    :param instance: instance stable id
    :param types: types to filter
    :return: Json dictionary object
    """

    headers = {
        'accept': 'application/json',
    }

    params = (
        ('types', types),
    )

    url = 'https://reactome.org/ContentService/search/diagram/%s/occurrences/%s' % (diagram, instance)

    try:
        response = requests.get(url=url, headers=headers, params=params)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print('Status code returned a value of %s' % response.status_code)


def search_diagram_pathway_flag(diagram='R-HSA-446203', query='CTSA'):
    """
    This method traverses the content and checks not only for the main identifier but also for all the cross-references to find the flag targets

    :param diagram: diagram/pathway stable id
    :param query: query names by this string
    :return: Json dictionary object of diagram entities plus pathways from the provided list containing the specified identifier
    """

    headers = {
        'accept': 'application/json',
    }

    params = (
        ('query', query),
    )

    url = 'https://reactome.org/ContentService/search/diagram/%s/flag' % diagram

    try:
        response = requests.get(url=url, headers=headers, params=params)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print('Status code returned a value of %s' % response.status_code)


def search_facet():
    """
    This method retrieves faceting information on the whole Reactome search data.

    :return: Json dictionary object of all facets corresponding to the whole Reactome search data
    """

    headers = {
        'accept': 'application/json',
    }

    url = 'https://reactome.org/ContentService/search/facet'

    try:
        response = requests.get(url=url, headers=headers)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print('Status code returned a value of %s' % response.status_code)


def search_facet_query(query='TP53', species=[], types=[], compartments=[], keywords=[]):
    """
    This method retrieves faceting information on a specific query

    :param query: search term
    :param species:  Species identifier (it can be the taxonomy id, species name or dbId) - python list of strings
    :param types: types to filter by - python list of strings
    :param compartments: compartments - python list of strings
    :param keywords: keywords - python list of strings
    :return: Json dictionary object
    """

    headers = {
        'accept': 'application/json',
    }

    params = (
        ('query', query),
        ('species', species),
        ('types', types),
        ('compartments', compartments),
        ('keywords', keywords),
    )

    url = 'https://reactome.org/ContentService/search/facet_query'

    try:
        response = requests.get(url=url, headers=headers, params=params)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print('Status code returned a value of %s' % response.status_code)


def search_fireworks(query='BRAF', species='Homo sapiens', types=[], start=None, rows=None):
    """
    Performs a Apache Solr query (fireworks widget scoped) for a given QueryObject

    :param query: Search term
    :param species: Species identifier (it can be the taxonomy id, species name or dbId)
    :param types: Types to filter by - python list of strings
    :param start: Start row
    :param rows: Number of rows to include
    :return: Json dictionary object
    """

    headers = {
        'accept': 'application/json',
    }

    params = (
        ('query', query),
        ('species', species),
        ('types', types),
        ('start', start),
        ('rows', rows),
    )

    url = 'https://reactome.org/ContentService/search/fireworks'

    try:
        response = requests.get(url=url, headers=headers, params=params)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print('Status code returned a value of %s' % response.status_code)


def search_fireworks_flag(query='KNTC1', species='Homo sapiens'):
    """
    Performs a Apache Solr query (fireworks widget scoped) for a given QueryObject

    :param query: Search term
    :param species: Species identifier (it can be the taxonomy id, species name or dbId)
    :return: Json dictionary object
    """

    headers = {
        'accept': 'application/json',
    }

    params = (
        ('query', query),
        ('species', species),
    )

    url = 'https://reactome.org/ContentService/search/fireworks/flag'

    try:
        response = requests.get(url=url, headers=headers, params=params)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print('Status code returned a value of %s' % response.status_code)


def search_query(query='Biological oxidations', species=[], types=[], compartments=[], keywords=[], cluster=True,
                 start=None, rows=None):
    """
    This method performs a Solr query on the Reactome knowledgebase. Results can be provided in a paginated format.

    :param query: term to search
    :param species: list of species - python list of strings
    :param types: Types to filter by - python list of strings
    :param compartments: Compartments - python list of strings
    :param keywords: Keywords - python list of strings
    :param cluster: Cluster results
    :param start: Start row
    :param rows: number of rows to include
    :return: Json dictionary object
    """

    headers = {
        'accept': 'application/json',
    }

    params = (
        ('query', query),
        ('species', species),
        ('types', types),
        ('compartments', compartments),
        ('keywords', keywords),
        ('cluster', cluster),
        ('Start row', start),
        ('rows', rows),
    )

    url = 'https://reactome.org/ContentService/search/query'

    try:
        response = requests.get(url=url, headers=headers, params=params)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print('Status code returned a value of %s' % response.status_code)


def search_spellcheck(query='repoduction'):
    """
    This method retrieves a list of spell-check suggestions for a given search term.

    :param query: term to search
    :return: list of matched elements
    """
    headers = {
        'accept': 'application/json',
    }

    params = (
        ('query', query),
    )

    url = 'https://reactome.org/ContentService/search/spellcheck'

    try:
        response = requests.get(url=url, headers=headers, params=params)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print('Status code returned a value of %s' % response.status_code)


def search_suggest(query='platele'):
    """
    This method retrieves a list of suggestions for a given search term.

    :param query: term to search
    :return: list of matched elements
    """

    headers = {
        'accept': 'application/json',
    }

    params = (
        ('query', query),
    )

    url = 'https://reactome.org/ContentService/search/suggest'

    try:
        response = requests.get(url=url, headers=headers, params=params)
    except ConnectionError as e:
        print(e)

    if response.status_code == 200:
        return response.json()
    else:
        print('Status code returned a value of %s' % response.status_code)