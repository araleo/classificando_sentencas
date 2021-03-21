""" Módulo para realizar pesquisas textuais entre as sentenças já classificadas. """


import os
import sys

from unidecode import unidecode
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import pandas as pd

from Util.rol_varas import LISTA_VARAS
from Util.util import load_category


def load_files(root):
    """
    Recebe um diretório para leitura.
    Retorna um dicionário do tipo d[vara][categoria][num_processo] = sentença
    para todas as sentenças em subdiretórios do diretório root.
    """
    d = dict()
    for vara in os.listdir(root):
        d[vara] = {}
        for categoria in os.listdir(f"{root}/{vara}"):
            if not categoria == "3":
                cat = load_category(categoria)
                for sent in os.listdir(f"{root}/{vara}/{categoria}"):
                    with open(f"{root}/{vara}/{categoria}/{sent}", "r") as f:
                        conteudo = f.read()
                        d[vara].setdefault(cat, {})
                        d[vara][cat][sent[:20]] = conteudo
    return d


def total_varas(d, varas, tipo):
    """
    Recebe um dicionário, uma lista de strings com varas e uma string com um tipo.
    Retorna o total de sentenças do tipo entre as varas encontradas no dicionário.
    """
    return sum([len(d[vara][tipo]) for vara in varas if tipo in d[vara]])


def total_sentencas(d):
    """Recebe um dicionário e retorna o total de sentenças encontradas nele."""
    tipos = ["absolutorias", "condenatorias", "neutras"]
    return sum([total_varas(d, list(d), tipo) for tipo in tipos])


def validate_vara(varas):
    """
    Recebe uma lista de strings contendo varas.
    Retorna a LISTA_VARAS se a primeira string da lista == "todas".
    Senão, retorna uma lista com as varas que estão na lista
    passada como parâmetro e também estão na LISTA_VARAS.
    """
    return LISTA_VARAS if varas[0] == "todas" else [vara for vara in varas if vara in LISTA_VARAS]


def calc_pcts(qtds, query):
    """
    Recebe um dicionário com quantidades.
    Retorna um dicionário contendo porcentagens
    para cada tipo de sentença e para a query.
    """
    pct = dict()
    pct["query"] = 100 * qtds[query] / qtds["pesquisadas"]
    pct["abs"] = 100 * qtds.get("absolutorias", 0) / qtds[query] if pct["query"] != 0 else 0
    pct["con"] = 100 * qtds.get("condenatorias", 0) / qtds[query] if pct["query"] != 0 else 0
    pct["neu"] = 100 * qtds.get("neutras", 0) / qtds[query] if pct["query"] != 0 else 0
    return pct


def query_finder(query, sent):
    """
    Recebe uma string query e um texto.
    Retorna True se todos os termos de query foram encontrados em sent.
    """
    return len([x for x in set(query.split()) if f" {x} " in sent]) == len(query.split())


def corpus_search(d, query, juizos, tipos):
    """
    Recebe um dicionário d, uma string query,
    uma lista com varas e uma com tipos.
    Retorna uma tupla com dois dicionários:
    matches contém as sentenças que contém query
    e são de um dos juízos e de um dos tipos,
    qtds contém a quantidade de cada tipo pesquisado.
    """
    qtds = {"pesquisadas": 0, "absolutorias": 0, "condenatorias": 0, "neutras": 0}
    matches = {"absolutorias": {}, "condenatorias": {}, "neutras": {}}
    for juizo in juizos:
        for tipo in tipos:
            for numero, sentenca in d[juizo][tipo].items():
                qtds["pesquisadas"] += 1
                if query_finder(query, sentenca):
                    matches[tipo][numero] = sentenca
                    qtds[tipo] += 1
    qtds[query] = qtds.get("absolutorias", 0) + qtds.get("condenatorias", 0) + qtds.get("neutras", 0)
    return matches, qtds


def sent_finder(sentencas, query):
    """
    Recebe um dicionário do tipo d = {num_processo: sentença}
    e uma string query.
    Retorna uma tupla contendo um numero de processo e uma sentença,
    classificada de acordo com o tf_idf das sentenças.
    ** Essa função ignora por enquanto o idf, que será implementado posteriormente **
    """
    idfs, tfidfs = compute_tf_idfs(sentencas)
    scores = {}
    for num, sent in sentencas.items():
        score = 0
        for word in set(query.split()):
            score += tfidfs.loc[num, word]
        scores[num] = score
    top = sorted(scores, key=scores.get, reverse=True)[0]
    return top, sentencas[top]


def compute_tf_idfs(docs):
    """
    Recebe um dicionário do tipo d = {num_processo: sentença}.
    Calcula o idf e o tf_idf e os retorna em uma tupla de dois pd.DataFrames
    """
    nums = list(docs)
    sents = list(docs.values())
    cv = CountVectorizer()
    word_count = cv.fit_transform(sents)
    transformer = TfidfTransformer(smooth_idf=True, use_idf=True)
    transformer.fit(word_count)
    idfs_df = pd.DataFrame(transformer.idf_, index=cv.get_feature_names(), columns=["idf_weights"])

    tf_idf_vector = transformer.transform(word_count)
    tf_idfs_df = pd.DataFrame(tf_idf_vector.todense(), index=nums, columns=cv.get_feature_names())

    return idfs_df, tf_idfs_df


def main():
    print("Carregando dados...")
    d = load_files(f"./{sys.argv[1]}")
    numero_sentencas = total_sentencas(d)
    print(f"Dados carregados! Foram carregadas {numero_sentencas} sentenças.")

    while True:
        query = input("Busca: ")
        query = unidecode(query).lower()
        juizos = validate_vara(input("Vara: ").split())
        tipos = ["absolutorias", "condenatorias", "neutras"]

        if len(juizos) == 0:
            print("Nenhuma das varas pesquisadas foi encontrada em nosso banco.")
            sys.exit()

        sents, qtds = corpus_search(d, query, juizos, tipos)
        pct = calc_pcts(qtds, query)

        output = (
            f"Foram pesquisadas {qtds['pesquisadas']} sentenças ",
            f"e o termo {query} foi encontrado em {qtds[query]} delas ",
            f"({pct['query']:.2f}%).\n",
            f"Das {qtds[query]} sentenças encontradas, ",
            f"{qtds.get('absolutorias', 0)} absolutorias ({pct['abs']:.2f}%), ",
            f"{qtds.get('condenatorias', 0)} condenatorias ({pct['con']:.2f}%) e "
            f"{qtds.get('neutras', 0)} neutras ({pct['neu']:.2f}%)."
        )
        print("".join(output))

        cat = load_category(input("Deseja visualizar uma sentença? 0. Neutra 1. Absolutoria 2. Condenatoria 3. Não"))
        if cat:
            print(sent_finder(sents[cat], query))


if __name__ == "__main__":
    main()
