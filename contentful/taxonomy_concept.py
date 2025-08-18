from .resource import Resource


class TaxonomyConcept(Resource):
    """
    Represents a single taxonomy concept.
    """

    def __init__(self, item, **kwargs):
        super(TaxonomyConcept, self).__init__(item, **kwargs)
        self.uri = item.get('uri')
        self.pref_label = item.get('prefLabel', {})
        self.alt_labels = item.get('altLabels', {})
        self.hidden_labels = item.get('hiddenLabels', {})
        self.notations = item.get('notations', [])
        self.note = item.get('note', {})
        self.change_note = item.get('changeNote', {})
        self.definition = item.get('definition', {})
        self.editorial_note = item.get('editorialNote', {})
        self.example = item.get('example', {})
        self.history_note = item.get('historyNote', {})
        self.scope_note = item.get('scopeNote', {})
        self.broader = item.get('broader', [])
        self.related = item.get('related', [])
        self.concept_schemes = item.get('conceptSchemes', [])

    def __repr__(self):
        return "<TaxonomyConcept id='{0}'>".format(
            self.sys.get('id', '')
        )
