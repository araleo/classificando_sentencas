import os
import string

from nltk.classify import ClassifierI
from unidecode import unidecode
import nltk


STOPLIST = nltk.corpus.stopwords.words("portuguese") + list(string.punctuation) + ["–"]


class VoteClassifier(ClassifierI):
    def __init__(self, classifiers):
        self._classifiers = classifiers

    def votes(self, features):
        return [c.classify(features) for c in self._classifiers]

    def classify(self, features):
        votes = self.votes(features)
        v = {i: votes.count(i) for i in range(3)}
        return max(v, key=v.get)

    def confidence(self, features):
        votes = self.votes(features)
        return votes.count(self.classify(features)) / len(votes)

    def safe_classify(self, features, n):
        _class = self.classify(features)
        _confidence = self.confidence(features)
        return (_class, _confidence) if _confidence >= n else (None, None)


class Sentencas():
    def __init__(self, path):
        self.sentencas = self.reader(path)

    def reader(self, path):
        sentencas = set()
        for file in os.listdir(path):
            file_path = path + "/" + file
            with open(file_path, "r") as f:
                conteudo = f.read()
                s = Sentenca(self.preprocess(conteudo))
                sentencas.add(s)
        return sentencas

    def preprocess(self, texto):
        words = [w.lower() for w in texto.split()]
        return " ".join(words)


class Sentenca():
    def __init__(self, texto):
        self._texto = texto

    def tokens(self):
        return [t.lower() for t in nltk.word_tokenize(self._texto) if t.lower() not in STOPLIST]

    def decoded_tokens(self):
        return [unidecode(t) for t in self.tokens()]

    def find_query(self, query):
        return unidecode(query.lower()) in self.decoded_tokens()

