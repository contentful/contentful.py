from .resource import Resource


class TaxonomyConceptScheme(Resource):
    """
    Represents a single taxonomy concept scheme.
    """

    def __init__(self, item, **kwargs):
        super(TaxonomyConceptScheme, self).__init__(item, **kwargs)
        self.uri = item.get('uri')
        self.pref_label = item.get('prefLabel', {})
        self.definition = item.get('definition', {})
        self.top_concepts = item.get('topConcepts', [])
        self.concepts = item.get('concepts', [])
        self.total_concepts = item.get('totalConcepts')

    def __repr__(self):
        return "<TaxonomyConceptScheme id='{0}'>".format(
            self.sys.get('id', '')
        )
