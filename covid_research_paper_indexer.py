import sys

sys.path.append('es_core/')
sys.path.append('top_search/')
sys.path.append('datasets/')
from query_handler import QueryHandler
import top_search


class Indexer:
    def __init__(self):
        self.query = QueryHandler()
        pass

    def search_paper(self, query):
        """
        Search paper indexed using ES lucene
        :param query: The query string
        :return: List of papers matching query
        """
        hits = self.query.lite_search(query)
        result = []
        for hit in hits:
            hit_source = hit['_source']
            top_search.update_count(hit_source["document_id"], hit_source["title"],
                                    hit_source["abstract"], hit_source["research_paper_url"])
            res = {
                "title": hit_source["title"],
                "abstract": hit_source["abstract"],
                "url": hit_source["research_paper_url"]
            }
            result.append(res)
        return result

    @staticmethod
    def top_searches(start=0, end=10):
        """
        Return top searched papers
        :param start: for pagination start
        :param end: pagination end
        :return: list of papers ordered by search count.
        """
        return top_search.top_search_impl(start, end)
