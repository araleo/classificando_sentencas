""" Módulo para treino dos classificadores e classificação de novos dados. """


import os
import random

import nltk

from classificadores import classifiers_list
from Sentencas import Sentencas, STOPLIST
from VoteClassifier import VoteClassifier
from util import set_outfolder, write_outfile


def document_features(tokens, word_features):
    """
    Recebe uma lista de tokens e uma lista de features.
    Retorna o dicionário de features no texto.
    """
    document_words = set(tokens)
    return {word: word in document_words for word in word_features}


def get_features(text, word_features):
    """
    Recebe uma string e uma lista de features.
    Retorna o dicionario de features do texto.
    """
    tokens = [t.lower() for t in nltk.word_tokenize(text) if t not in STOPLIST]
    return document_features(tokens, word_features)


def classificador(classifier, word_features, root, out):
    """
    Recebe um VoteClassifier, uma lista de features,
    um diretório para leitura e um para gravação.
    Classifica todos os arquivos encontrados em
    subdiretórios do subdiretório passado como paramêtro.
    Grava os resultados no diretório de gravação.
    """
    for folder in os.listdir(root):
        print(folder)
        folder_path = f"{root}/{folder}"
        for file in os.listdir(folder_path):
            fp = f"{folder_path}/{file}"
            with open(fp, "r") as f:
                conteudo = f.read()
                f_features = get_features(conteudo, word_features)
                f_class, _ = classifier.safe_classify(f_features, 1)
                outfolder = set_outfolder(f_class, out, folder)
                write_outfile(f"{outfolder}/{file}", conteudo)


def get_train_test_sets(feature_set):
    """
    Recebe uma lista de tuplas (features, classificação).
    Embaralha a lista e divide no meio.
    Retorna um train_set e um test_set.
    """
    random.shuffle(feature_set)
    size = len(feature_set)
    train_set, test_set = feature_set[size//2:], feature_set[:size//2]
    return train_set, test_set


def train_classifiers(train_set, test_set):
    """
    Recebe duas listas de tuplas (features, classificação).
    Treina os classificadores da variável classifiers_list individualmente.
    """
    for classifier in classifiers_list:
        classifier.train(train_set)
        print(classifier, nltk.classify.accuracy(classifier, test_set))


def def_vote_classifier(test_set):
    """
    Recebe uma lista de tuplas (features, classificação) para teste.
    Treina um classificador da classe VoteClassifier
    a partir dos classificadores individuais já treinados
    Retorna um classificador VoteClassifier.
    """
    vote_classifier = VoteClassifier(classifiers_list)
    print("voted: ", nltk.classify.accuracy(vote_classifier, test_set))
    return vote_classifier


def main():
    # carrega as sentenças na memoria
    absolutorias = Sentencas("./OSC/labels/absolutorias")
    condenatorias = Sentencas("./OSC/labels/condenatorias")
    neutras = Sentencas("./OSC/labels/neutras")

    # cria lista com todas as 3000 palavras mais frequentes em todas as sentenças
    all_words = nltk.FreqDist(absolutorias.tokens() + condenatorias.tokens() + neutras.tokens())
    word_features = list(all_words)[:3000]

    # cria lista de (features , classificacao)
    a_set = [(document_features(s.tokens(), word_features), 1) for s in absolutorias.sentencas]
    c_set = [(document_features(s.tokens(), word_features), 2) for s in condenatorias.sentencas]
    n_set = [(document_features(s.tokens(), word_features), 0) for s in neutras.sentencas]
    feature_set = a_set + c_set + n_set

    # embaralha e divide o set
    train_set, test_set = get_train_test_sets(feature_set)

    # treina cada classificador
    train_classifiers(train_set, test_set)

    # carrega os classificadores no objeto para votar e classificar
    vote_classifier = def_vote_classifier(test_set)

    classificador(vote_classifier, word_features, "./raw", "./OSC/corpus")


if __name__ == "__main__":
    main()
