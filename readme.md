ES Index for research papers submitted under Coronavirus Category..

## Setup
Run all the scripts under installation.

## Basic usage

Index the papers by running ``` index_abstracts.py```


Example:
```buildoutcfg
from covid_research_paper_indexer import Indexer
idx = Indexer()

# Search papers
result = idx.search_paper('incubation period of covid19')

# Top Searches
top = idx.top_searches()
```
