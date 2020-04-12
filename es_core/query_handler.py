"""
Query Handler for es.
"""

from elasticsearch import Elasticsearch

import constants
from content_handler import ContentHandler


class QueryHandler:
    # TODO: Query Interface for deep doc search.

    def __init__(self):
        self.es = Elasticsearch()
        self.ch = ContentHandler()

    def lite_search(self, query):
        if not isinstance(query, str):
            return []
        processed_query = self.ch.transform(query)
        if processed_query == '':
            return []
        # TODO: Proper tf-idf freq.
        res = self.es.search({
            "query": {
                "more_like_this": {
                    "fields": ["title_index", "abstract_index"],
                    "like": processed_query,
                    "min_term_freq": 1,
                    "max_query_terms": 15,
                    "min_doc_freq": 1
                }
            }
        }, index=constants.DEFAULT_LITE_INDEX)
        return res["hits"]["hits"]
