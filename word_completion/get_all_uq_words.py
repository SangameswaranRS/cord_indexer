"""
Get all unique words.
"""

import sys

import pandas as pd

sys.path.append('../es/datasets/')
sys.path.append('../es/es_core/')
from content_handler import ContentHandler
import dataset_config

file_path = ''
ch = ContentHandler()
if len(sys.argv) > 1:
    file_path = sys.argv[1]
else:
    print('[ERROR] Specify file path in the command line arg')
    sys.exit(1)


def encoding_check(wrd):
    try:
        wrd.encode(encoding='utf-8').decode('ascii')
        return True
    except Exception:
        return False


def lev2_clean(wd):
    tr_filter = '!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n'
    w2 = wd.translate(str.maketrans(tr_filter, len(tr_filter) * " "))
    if encoding_check(w2):
        return wd
    return None


df = pd.read_csv(file_path)
assert df is not None
word_set = set()
for i in range(0, df.shape[0]):
    print('[INFO] Processing ' + str(i) + "/" + str(df.shape[0]))
    row = list(df.iloc[i])
    title = row[dataset_config.GLOBAL_INDEX[dataset_config.ABSTRACTS]["titleIndex"]]
    abstract = row[dataset_config.GLOBAL_INDEX[dataset_config.ABSTRACTS]["abstractIndex"]]
    title_transformed = ch.transform(title)
    abstract_transformed = ch.transform(abstract)
    for title_tokens in ch._get_tokens(title_transformed):
        w = lev2_clean(title_tokens)
        if w is not None:
            word_set.add(lev2_clean(title_tokens))
    for abstract_token in ch._get_tokens(abstract_transformed):
        w = lev2_clean(abstract_token)
        if w is not None:
            word_set.add(w)

print('[INFO] word_set generated: ' + str(len(word_set)))
file = open('unique_words.txt', 'w+')
for word in word_set:
    file.write(word + '\n')
file.close()
