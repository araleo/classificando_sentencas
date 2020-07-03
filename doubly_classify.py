import nltk

from classify import document_features, get_train_test_sets, train_classifiers, classificador, def_vote_classifier
from Sentencas import Sentencas
from corpus_transfer import move_nc


def classify_nao_condenatorias():
    absolutorias = Sentencas("./TCTS/labels_a_n/absolutorias")
    neutras = Sentencas("./TCTS/labels_a_n/neutras")

    all_words = nltk.FreqDist(absolutorias.tokens() + neutras.tokens())
    word_features = list(all_words)[:3000]

    c_set = [(document_features(s.tokens(), word_features), 1) for s in absolutorias.sentencas]
    nc_set = [(document_features(s.tokens(), word_features), 0) for s in neutras.sentencas]
    feature_set = c_set + nc_set

    train_set, test_set = get_train_test_sets(feature_set)

    train_classifiers(train_set, test_set)
    vote_classifier = def_vote_classifier(test_set)

    classificador(vote_classifier, word_features, "./TCTS/nc", "./TCTS/classified_a_n")


def classify_condenatorias():
    condenatorias = Sentencas("./TCTS/labels_c_nc/condenatorias")
    nao_condenatorias = Sentencas("./TCTS/labels_c_nc/naocondenatorias")

    all_words = nltk.FreqDist(condenatorias.tokens() + nao_condenatorias.tokens())
    word_features = list(all_words)[:3000]

    c_set = [(document_features(s.tokens(), word_features), 1) for s in condenatorias.sentencas]
    nc_set = [(document_features(s.tokens(), word_features), 0) for s in nao_condenatorias.sentencas]
    feature_set = c_set + nc_set

    train_set, test_set = get_train_test_sets(feature_set)

    train_classifiers(train_set, test_set)
    vote_classifier = def_vote_classifier(test_set)

    classificador(vote_classifier, word_features, "./raw", "./TCTS/classified_c_nc")


def main():
    classify_condenatorias()
    move_nc("./TCTS/classified_c_nc", "./TCTS/nc")
    classify_nao_condenatorias()


if __name__ == "__main__":
    main()
