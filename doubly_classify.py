"""
Módulo principal para classificação utilizado no projeto de classificação de sentenças criminais.
Primeiro classifica todas as sentenças entre condenatórias e não condenatórias.
Em seguida classifica as não condenatórias entre absolutórias e neutras.
"""


import nltk

from classify import document_features, get_train_test_sets, train_classifiers, classificador, def_vote_classifier
from corpus_transfer import move_nc, move_condenatorias, move_abs_e_neutras
from Sentencas import Sentencas
from util import make_folder


def bin_classify(grupo_zero, grupo_um, infolder, outfolder):
    """
    Função genérica de classificação entre sentenças de dois grupos
    Recebe dois objetos da classe Sentenca, um diretório para leitura e um para gravação
    """
    all_words = nltk.FreqDist(grupo_zero.tokens() + grupo_um.tokens())
    word_features = list(all_words)[:3000]

    set_0 = [(document_features(s.tokens(), word_features), 0) for s in grupo_zero.sentencas]
    set_1 = [(document_features(s.tokens(), word_features), 1) for s in grupo_um.sentencas]
    feature_set = set_0 + set_1

    train_set, test_set = get_train_test_sets(feature_set)
    train_classifiers(train_set, test_set)
    vote_classifier = def_vote_classifier(test_set)

    classificador(vote_classifier, word_features, infolder, outfolder)


def load_labels(labels_path):
    condenatorias = Sentencas(path=f"{labels_path}/condenatorias")
    absolutorias = Sentencas(path=f"{labels_path}/absolutorias")
    neutras = Sentencas(path=f"{labels_path}/neutras")
    return condenatorias, absolutorias, neutras


def make_temp_folders(temp_path):
    make_folder(f"{temp_path}/tempc")
    make_folder(f"{temp_path}/tempnc")
    make_folder(f"{temp_path}/tempholder")


def main():
    condenatorias, absolutorias, neutras = load_labels("./tributario/labels")
    nao_condenatorias = absolutorias + neutras

    make_temp_folders("./tributario/temp")
    bin_classify(nao_condenatorias, condenatorias, "./tributario/raw", "./tributario/temp/tempc")
    move_nc("./tributario/temp/tempc", "./tributario/temp/tempholder")
    bin_classify(neutras, absolutorias, "./tributario/temp/tempholder", "./tributario/temp/tempnc")

    move_condenatorias("./tributario/temp/tempc", f"./tributario/corpora/corpus")
    move_abs_e_neutras("./tributario/temp/tempnc", f"./tributario/corpora/corpus")


if __name__ == "__main__":
    main()
