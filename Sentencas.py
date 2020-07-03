import os
import string

import nltk


STOPLIST = nltk.corpus.stopwords.words("portuguese") + list(string.punctuation) + ["–"]


class Sentencas:
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

    def tokens(self):
        tokens = []
        for s in self.sentencas:
            t = s.tokens()
            tokens.extend(t)
        return tokens


class Sentenca:
    def __init__(self, texto):
        self.texto = texto

    def tokens(self):
        return [t.lower() for t in nltk.word_tokenize(self.texto) if t.lower() not in STOPLIST]
