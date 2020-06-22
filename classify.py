import os
import random

import nltk

from classificadores import classifiers_list
from util import Sentencas, VoteClassifier


def make_folder(path):
    try:
        os.makedirs(path)
    except FileExistsError:
        return None


def classificador(classifier, word_features):
    for folder in os.listdir("./scrap"):
        folder_path = f"./scrap/{folder}"
        for file in os.listdir(folder_path):
            fp = f"{folder_path}/{file}"
            with open(fp, "r") as f:
                conteudo = f.read()
                f_words = " ".join([w.lower() for w in conteudo.split()])
                f_features = document_features(f_words, word_features)
                f_class, _ = classifier.safe_classify(f_features, 1)
                if f_class is not None:
                    outfolder = f"./corpus/{folder}/{str(f_class)}"
                else:
                    outfolder = f"./corpus/{folder}/3"
                make_folder(outfolder)
                with open(f"{outfolder}/{file}", "w") as _f:
                    _f.write(conteudo)


def document_features(document, word_features):
    document_words = set(nltk.word_tokenize(document))
    return {word: word in document_words for word in word_features}


def main():
    # carrega as sentenças na memoria
    absolutorias = Sentencas("./labels/absolutorias")
    condenatorias = Sentencas("./labels/condenatorias")
    neutras = Sentencas("./labels/neutras")

    # cria lista com todas as 3000 palavras mais frequentes em todas as sentenças
    all_words = nltk.FreqDist(absolutorias.words() + condenatorias.words() + neutras.words())
    word_features = list(all_words)[:3000]

    # cria lista de (features , classificacao)
    a_set = [(document_features(s, word_features), 1) for s in absolutorias.sentencas]
    c_set = [(document_features(s, word_features), 2) for s in condenatorias.sentencas]
    n_set = [(document_features(s, word_features), 0) for s in neutras.sentencas]
    feature_set =  a_set + c_set + n_set

    # embaralha e divide o set
    random.shuffle(feature_set)
    size = len(feature_set)
    train_set, test_set = feature_set[size//2:], feature_set[:size//2]

    # treina cada classificador
    for classifier in classifiers_list:
        classifier.train(train_set)
        print(classifier, nltk.classify.accuracy(classifier, test_set))

    # carrega os classificadores no objeto para votar e classificar
    vote_classifier = VoteClassifier(classifiers_list)
    print("voted: ", nltk.classify.accuracy(vote_classifier, test_set))

    classificador(vote_classifier, word_features)


if __name__ == "__main__":
    main()
