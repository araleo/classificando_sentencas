""" Definição da classe VoteClassifier e do método safe_classify. """

from nltk.classify import ClassifierI


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
