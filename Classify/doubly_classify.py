"""
Módulo principal para classificação de sentenças criminais.
Primeiro classifica todas as sentenças entre condenatórias e não condenatórias.
Em seguida classifica as não condenatórias entre absolutórias e neutras.
"""


import nltk

from Classes.Sentencas import Sentencas
from classify import classificador
from classify import def_vote_classifier
from classify import document_features
from classify import get_train_test_sets
from classify import train_classifiers
from Util.corpus_transfer import move_abs_e_neutras
from Util.corpus_transfer import move_condenatorias
from Util.corpus_transfer import move_nc
from Util.util import make_folder


"""
Variáveis de diretórios
"""
raw_data_dir = "../Data/raw/jfrj"
labels_dir = "../Data/labels/labels3"
corpus_dir = "../Data/corpora/jfrj/classificadas"
temp_dir = "../Data/temp"
temp_dirs = {
    "con": temp_dir + "/tempc",
    "holder": temp_dir + "/tempholder",
    "ncon": temp_dir + "/tempnc"
}


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


def load_labels():
    condenatorias = Sentencas(path=f"{labels_dir}/condenatorias")
    absolutorias = Sentencas(path=f"{labels_dir}/absolutorias")
    neutras = Sentencas(path=f"{labels_dir}/neutras")
    return condenatorias, absolutorias, neutras


def make_temp_folders():
    make_folder(temp_dirs["con"])
    make_folder(temp_dirs["ncon"])
    make_folder(temp_dirs["holder"])


def main():
    condenatorias, absolutorias, neutras = load_labels()
    nao_condenatorias = absolutorias + neutras

    make_temp_folders()
    bin_classify(nao_condenatorias, condenatorias, raw_data_dir, temp_dirs["con"])
    move_nc(temp_dirs["con"], temp_dirs["holder"])
    bin_classify(neutras, absolutorias, temp_dirs["holder"], temp_dirs["ncon"])

    move_condenatorias(temp_dirs["con"], corpus_dir)
    move_abs_e_neutras(temp_dirs["ncon"], corpus_dir)


if __name__ == "__main__":
    main()
