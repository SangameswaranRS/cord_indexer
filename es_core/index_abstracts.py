"""
Index documents to elastic search.
"""

import sys
from pprint import pprint

import pandas as pd
from elasticsearch import Elasticsearch

import constants
from content_handler import ContentHandler

sys.path.append('../datasets/')
import dataset_config

es = Elasticsearch()
ch = ContentHandler()

es.indices.create(constants.DEFAULT_LITE_INDEX, ignore=[constants.ErrorConstants.INDEX_EXISTS])
print('[INFO] Index created')
print('[INFO] Reading abstracts')
docs_to_be_indexed = []
df = pd.read_csv(constants.ABSTRACTS_CSV_PATH)

for i in range(0, df.shape[0]):
    print('[INFO] Preparing data  :' + str(i) + "/" + str(df.shape[0]))
    row = list(df.iloc[i])
    document_id = row[dataset_config.GLOBAL_INDEX[dataset_config.ABSTRACTS]["documentIdIndex"]]
    title = row[dataset_config.GLOBAL_INDEX[dataset_config.ABSTRACTS]["titleIndex"]]
    abstract = row[dataset_config.GLOBAL_INDEX[dataset_config.ABSTRACTS]["abstractIndex"]]
    paper_link = row[dataset_config.GLOBAL_INDEX[dataset_config.ABSTRACTS]["researchPaperUrlIndex"]]
    title_index = ch.transform(title)
    abstract_index = ch.transform(abstract)
    max_ranking_text = ch.extract_high_ranked_phrase(abstract)
    # Index operation meta information
    docs_to_be_indexed.append({'index': {'_id': document_id, '_index': constants.DEFAULT_LITE_INDEX}})
    # Body
    docs_to_be_indexed.append({
        'document_id': document_id,
        'title': title,
        'abstract': abstract,
        'research_paper_url': paper_link,
        'title_index': title_index,
        'abstract_index': abstract_index,
        'max_ranking_phrase': max_ranking_text
    })
    # FIXME: sanga.s
    if i > 1000:
        break

pprint(docs_to_be_indexed[:2])
print('[INFO] document list prepared')
print('[INFO] Indexing to elastic search')
res = es.bulk(docs_to_be_indexed, ignore=[constants.ErrorConstants.DOC_ALREADY_CREATED])
print('[INFO] Index created')
