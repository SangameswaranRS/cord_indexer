#!/bin/bash

cd ..
sudo python3 -m pip install -r requirements.txt
sudo python3 -m nltk.downloader stopwords
sudo python3 -m spacy download en_core_web_sm