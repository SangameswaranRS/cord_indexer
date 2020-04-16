"""
    Content Handler class.
"""

import os
import sys

import nltk
import pandas as pd
import pytextrank
import spacy
from gensim.models import Word2Vec
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

import constants

sys.path.append('../datasets/')
import dataset_config


class ContentHandler:
    def __init__(self, sl_flag=1, should_remove_stop_words=True):
        """
        Initialize handler.
        :param sl_flag: stem/lemmatize flag - 0: stem 1: lemmatize
        :param should_remove_stop_words: default: True
        """
        nltk.download('stopwords')
        nltk.download('punkt')
        nltk.download('wordnet')
        self.sl_flag = sl_flag
        if sl_flag not in [0, 1]:
            raise ValueError("Invalid sl flag provided")
        self.should_remove_stop_words = should_remove_stop_words
        self.porter_stemmer = PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        self.punctuation_filters = '!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n'
        self.tr = pytextrank.TextRank()
        # FIXME: sanga.s add abstractive techniques.
        # pytext rank computes similarity graph and returns
        # important sentence as the one that is most similar to all.
        self.spacy_pipeline = spacy.load("en_core_web_sm")
        self.spacy_pipeline.add_pipe(self.tr.PipelineComponent, name="TextRank", last=True)
        self.word2vec_trained = os.path.exists(constants.WORD2VEC_MODEL_PATH)
        if not self.word2vec_trained:
            self.train_word2vec()
        self.word2vec_model = self.retrieve_model()

    def _remove_stop_words(self, text):
        candidate_tokens = word_tokenize(text)
        filtered_list = [word for word in candidate_tokens if not word in self.stop_words]
        return ' '.join(filtered_list)

    def _get_tokens(self, text):
        text = self._remove_stop_words(text)
        text = text.lower()
        text_trans = text.translate(str.maketrans(self.punctuation_filters, " " * len(self.punctuation_filters)))
        token_list = text_trans.split(" ")
        return [token for token in token_list if token]

    def transform(self, text):
        """
        Tokenize and transform text.
        :param text: text type:str
        :return: transformed str.
        """
        if not isinstance(text, str):
            # raise ValueError('str expected got ' + str(type(text) + ' instead'))
            return ""
        text_tokens = self._get_tokens(text)
        result = ''
        if text_tokens is not None and len(text_tokens) > 0:
            for i in range(0, len(text_tokens)):
                if self.sl_flag == 1:
                    result += self.lemmatizer.lemmatize(text_tokens[i]) + ' '
                else:
                    result += self.lemmatizer.lemmatize(text_tokens[i]) + ' '
        return result

    def extract_high_ranked_phrase(self, text):
        """
        Extract high ranked phrase.
        :param text: text
        :return: the high ranked phrase
        """
        if not isinstance(text, str):
            # raise ValueError('str expected got ' + str(type(text)) + ' instead')
            return ""
        sp_result = self.spacy_pipeline(text)
        return str(sp_result._.phrases[0])

    def get_keywords(self, query):
        """
        Get keywords for query.
        :param query: The query
        :return: list of keywords
        """
        if not self.word2vec_trained:
            print('[ERROR] Word 2 vec model not trained')
            return []
        model = self.word2vec_model
        keyword_list = []
        query_transformed = self.transform(query)
        query_tokens = query_transformed.split(" ")
        # print(query_tokens)
        for token in query_tokens:
            most_similar = model.wv.most_similar(positive=token, topn=5)
            for ms_entity in most_similar:
                keyword_list.append(ms_entity[0])
        return keyword_list

    def retrieve_model(self):
        if os.path.exists(constants.WORD2VEC_MODEL_PATH):
            self.word2vec_trained = True
            model = Word2Vec.load(constants.WORD2VEC_MODEL_PATH)
            return model

    def train_word2vec(self):
        df = pd.read_csv(constants.ABSTRACTS_CSV_PATH)
        word2vec_doc_list = []
        for i in range(0, df.shape[0]):
            print('[INFO] i ' + str(i))
            row = list(df.iloc[i])
            title = row[dataset_config.GLOBAL_INDEX[dataset_config.ABSTRACTS]["titleIndex"]]
            abstract = row[dataset_config.GLOBAL_INDEX[dataset_config.ABSTRACTS]["abstractIndex"]]
            title_abstract_transformed = self.transform(title) + self.transform(abstract)
            token_list = title_abstract_transformed.split(" ")
            word2vec_doc_list.append(token_list)

        print('[INFO] Model training.')
        model = Word2Vec(word2vec_doc_list, window=5, workers=5, size=100)

        print('[INFO] Training done.')
        model.save(constants.WORD2VEC_MODEL_PATH)
        print('[INFO] Model serialized')
