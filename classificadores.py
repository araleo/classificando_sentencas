"""
Módulo para carregar os classificadores.
Cria uma lista classifiers_list, contendo classificadores para uso.
Atualmente: [LSVC, SGD].
"""


from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import SGDClassifier
from sklearn.svm import LinearSVC


MNB = SklearnClassifier(MultinomialNB())
BNB = SklearnClassifier(BernoulliNB())
SGD = SklearnClassifier(SGDClassifier())
LSVC = SklearnClassifier(LinearSVC(dual=False))
classifiers_list = [LSVC, SGD]
# classifiers_list = [MNB, BNB, SGD, LSVC]
