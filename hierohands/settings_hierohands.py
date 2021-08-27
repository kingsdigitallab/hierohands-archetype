# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# PROJECT settings
# PLEASE DO NOT PLACE ANY SENSITIVE DATA HERE (password, keys, personal
# data, etc.)
# Use local_settings.py for that purpose

# Lightbox
"""
The Lightbox is a separate project, even though it's still tightly linked to Digipal. It is possible to install it through pip:
>>> pip install git+https://github.com/Gbuomprisco/Digital-Lightbox.git
By default, it is disabled. You can enable it by setting the variable LIGHTBOX in your settings:
"""
LIGHTBOX = True

# Mezzanine
SITE_TITLE = 'Hieroglyphic Hands'

# Social
"""
The following variables contains the URLs/username to social networking sites.
- The TWITTER variable asks for the Twitter username.
- The GITHUB variable asks for the relative URL to your Github project or account
- The COMMENTS_DISQUS_SHORTNAME asks for the Disqus shortname
"""
TWITTER = ''
GITHUB = ''
# COMMENTS_DISQUS_SHORTNAME = "exondomesday"

# Annotator Settings

"""
If True, this setting will reject every change to the DB. To be used in production websites.
"""
REJECT_HTTP_API_REQUESTS = False  # if True, prevents any change to the DB

"""
This setting allows to set the number of zoom levels available in the OpenLayers layer.
"""
ANNOTATOR_ZOOM_LEVELS = 7  # This setting sets the number of zoom levels of O

FOOTER_LOGO_LINE = True

# Customise the faceted search settings
MODELS_PRIVATE = ['itempart', 'image', 'graph', 'hand', 'textcontentxml']
MODELS_PUBLIC = MODELS_PRIVATE

DEBUG_PERFORMANCE = False
COMPRESS_ENABLED = True
# COMPRESS_ENABLED = True

# from customisations.digipal.views.faceted_search.settings import FACETED_SEARCH

# CUSTOM_APPS = ['exon.customisations.mapping']

TEXT_IMAGE_MASTER_CONTENT_TYPE = 'transcription'
KDL_MAINTAINED = True

TEXT_EDITOR_OPTIONS_CUSTOM2 = {
    'buttons': {
        'btnPersonName': {'label': 'Person name', 'tei': '<rs type="person" subtype="name">{}</rs>'},
        'btnPersonMaritalStatus': {'label': 'Marital status', 'tei': '<rs type="person" subtype="marital-status">{}</rs>'},
        'btnPerson': {'label': 'Person', 'buttons': ['btnPersonName', 'btnPersonMaritalStatus']},

        'btnPlaceName': {'label': 'Place name', 'tei': '<rs type="place" subtype="name">{}</rs>'},
        'btnBirthPlace': {'label': 'Birth place', 'tei': '<rs type="place" subtype="birthplace">{}</rs>'},
        'btnResidence': {'label': 'Residence', 'tei': '<rs type="place" subtype="residence">{}</rs>'},
        'btnPlace': {'label': 'Place', 'buttons': ['btnPlaceName', 'btnBirthPlace', 'btnResidence']},

        'btnDate': {'label': 'Date', 'tei': '<rs type="date">{}</rs>'},
        'btnOccupation': {'label': 'Occupation', 'tei': '<rs type="occupation">{}</rs>'},

        'btnReligion': {'label': 'Religion', 'tei': '<rs type="religion">{}</rs>'},
        'btnReligiousStatus': {'label': 'Religious status', 'tei': '<rs type="religious-status">{}</rs>'},

        'btnJuridicalStatus': {'label': 'Juridical status', 'tei': '<rs type="juridical-status">{}</rs>'},
        'btnInfrastructure': {'label': 'Infrastructure', 'tei': '<rs type="infrastructure">{}</rs>'},
        'btnBuilding': {'label': 'Building', 'tei': '<rs type="building">{}</rs>'},
        'btnLand': {'label': 'Land', 'tei': '<rs type="land">{}</rs>'},
        'btnEconomicData': {'label': 'Economic Data', 'tei': '<rs type="economic-data">{}</rs>'},

        'btnFurniture': {'label': 'Furniture', 'tei': '<rs type="item" subtype="furniture">{}</rs>'},
        'btnClothing': {'label': 'Clothing', 'tei': '<rs type="item" subtype="clothing">{}</rs>'},
        'btnFood': {'label': 'Food', 'tei': '<rs type="item" subtype="food">{}</rs>'},
        'btnTool': {'label': 'Tool', 'tei': '<rs type="item" subtype="tool">{}</rs>'},
        'btnWritingMaterial': {'label': 'Writing material', 'tei': '<rs type="item" subtype="writing-material">{}</rs>'},
        'btnItem': {'label': 'Item', 'buttons': ['btnFurniture', 'btnClothing', 'btnFood', 'btnTool', 'btnWritingMaterial']},
    },
    'show_highlights_in_preview': 1,
    'toolbars': {
        'default': 'psclear undo redo pssave | pslocation | btnPerson btnPlace btnDate btnOccupation btnReligion btnReligiousStatus | btnJuridicalStatus btnInfrastructure btnBuilding btnLand btnEconomicData btnItem | code ',
    },
    'panels': {
        'north': {
            'ratio': 0.0
        },
        'east': {
            'ratio': 0.0
        },
    }
}

# customisation of the search page

from digipal.views.faceted_search.settings import (
    remove_fields_from_faceted_search, FacettedType
)

search_graphs = FacettedType.fromKey('graphs')

search_graphs.addFieldToOption('column_order', 'character', 'allograph')

def get_val_from_note(annotation, key):
    if not annotation:
        return ''
    import re
    ret = re.findall(
        r'\b'+re.escape(key)+r'\s*:\s*([^<\n$]+)',
        annotation.display_note or ''
    )
    if ret:
        return ret[0].strip()
    else:
        return ''


def get_mdc_from_graph(graph):
    ret = ''
    annotation = getattr(graph, 'annotation', None)
    if annotation:
        ret = get_val_from_note(annotation, 'mdc')
    if not ret and graph.group_id:
        annotation = getattr(graph.group, 'annotation', None)
        ret = get_val_from_note(annotation, 'mdc')
    return ret


def get_translation_from_annotation(annotation):
    return get_val_from_note(annotation, 'tla')


def get_transliteration_from_annotation(annotation):
    return get_val_from_note(annotation, 'tli')


def get_search_label_from_scribe(scribe):
    import re
    return re.sub(r'\(.*\)', r'', (scribe.name or '')).strip()


search_graphs.addField({
    'key': 'translation', 'label': 'Translation',
    'path': 'annotation', 'transform': get_translation_from_annotation,
    'viewable': True, 'type': 'title', 'search': True,
})
search_graphs.addFieldToOption('column_order', 'translation', 'character')
search_graphs.addField({
    'key': 'transliteration', 'label': 'Transliteration',
    'path': 'annotation', 'transform': get_transliteration_from_annotation,
    'viewable': True, 'type': 'title', 'search': True,
})
search_graphs.addFieldToOption('column_order', 'transliteration', 'character')

search_graphs.addField({
    'key': 'allograph_illustration', 'label': 'Allograph',
    'path': 'idiograph.allograph.illustration',
    'viewable': True, 'type': 'django_image',
    'max_size': 100,
})
search_graphs.addFieldToOption('column_order', 'allograph_illustration')

search_graphs.addField({
    'key': 'ductus', 'label': 'Ductus',
    'path': 'annotation.illustration_ductus',
    'viewable': True, 'type': 'django_image',
    'max_size': 100,
})
search_graphs.addFieldToOption('column_order', 'ductus')

search_graphs.addField({
    'key': 'scribe', 'label': 'Scribe',
    'path': 'hand.scribe', 'transform': get_search_label_from_scribe,
    'viewable': True, 'type': 'title', 'search': True,
    'filter': True, 'count': True,
})
search_graphs.addFieldToOption('column_order', 'scribe', 'hand_label')

search_graphs.addField({
    'key': 'group_thumbnail', 'label': 'Sign group',
    'path': 'group.annotation',
    'viewable': True, 'type': 'image',
    'max_size': 70,
})
search_graphs.addFieldToOption('column_order', 'group_thumbnail')
search_graphs.addField({
    'key': 'group_name', 'label': 'Sign Group',
    'path': '', 'transform': get_mdc_from_graph,
    'viewable': True, 'type': 'code', 'search': True,
})
search_graphs.addFieldToOption('column_order', 'group_name')

search_graphs.getField('repo_place')['path'] = 'annotation.image.item_part.current_item.repository.short_name'
search_graphs.getField('character')['search'] = True
search_graphs.getField('character')['type'] = 'title'
del search_graphs.getField('repo_place')['path_result']
search_graphs.getField('thumbnail')['label'] = 'Picture'

remove_fields_from_faceted_search(['allograph', 'repo_city', 'hi_date', 'hand_place', 'hand_label', 'locus'], 'graphs')

# add C,F and CF to graphs
empty_mappings = FacettedType.getFragment('field_mapping_empty')
search_graphs.addField({
    'key': 'component', 'label': 'Component', 'path': 'graph_components.all.component.name',
    'type': 'id', 'filter': True, 'count': True, 'multivalued': True, 'mapping': empty_mappings
})
search_graphs.addField({
    'key': 'feature', 'label': 'Feature', 'path': 'graph_components.all.features.all.name',
    'type': 'id', 'filter': True, 'count': True, 'multivalued': True, 'mapping': empty_mappings
})
search_graphs.addField({
    'key': 'cf', 'label': 'Component-Feature', 'path': 'get_component_feature_labels',
    'type': 'id', 'filter': True, 'count': True, 'multivalued': True, 'mapping': empty_mappings
})
# search_graphs.addField({
#     'key': 'aspect', 'label': 'Aspect', 'path': 'aspects.name',
#     'type': 'id', 'filter': True, 'count': True, 'multivalued': True, 'mapping': empty_mappings
# })

search_graphs.addFieldsToOption(
    'filter_order',
    ['component', 'feature', 'cf', 'scribe'],
    'character'
)

# rename types
search_images = FacettedType.fromKey('images')
search_images.options['label'] = 'Text block'
search_manuscript = FacettedType.fromKey('manuscripts')
search_manuscript.options['label'] = 'Wall'


def rename_field(faceted_type, fkey, new_label):
    field = faceted_type.getField(fkey)
    if field:
        field['label'] = new_label


for t in FacettedType.getAll():
    rename_field(t, 'repo_place', 'Tomb')
    rename_field(t, 'repo_city', 'City')
    rename_field(t, 'hi_date', 'Date')
    rename_field(t, 'shelfmark', 'Chamber')
    rename_field(t, 'locus', 'Wall')
    t.disableView('overview')

    for field_name in ['hi_date', 'hand_date']:
        field = t.getField(field_name)
        if field:
            field['filter'] = False
        fo = t.getOption('filter_order')
        if fo:
            try:
                fo.remove(field_name)
            except ValueError:
                pass

# remove date selector, not applicable to this
