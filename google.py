import os
import sys

from unidecode import unidecode

from rol_varas import LISTA_VARAS
from util import Sentencas


def load_category(cat):
    if cat == "0":
        return "neutras"
    elif cat == "1":
        return "absolutorias"
    elif cat == "2":
        return "condenatorias"


def load_files(root, varas):
    D = dict()
    for vara in varas:
        D[vara] = {}
        for categoria in os.listdir(f"{root}/{vara}"):
            if not categoria == "3":
                cat = load_category(categoria)
                D[vara][cat] = Sentencas(f"{root}/{vara}/{categoria}")
    return D


def total_varas(D, varas, tipo):
    return sum([len(D[vara][tipo].sentencas) for vara in varas if tipo in D[vara]])


def total_sentencas(D):
    tipos = ["absolutorias", "condenatorias", "neutras"]
    return sum([total_varas(D, list(D), tipo) for tipo in tipos])


def validate_vara(varas):
    if varas[0] == "todas":
        return LISTA_VARAS
    return [vara for vara in varas if vara in LISTA_VARAS]


def calc_pcts(qtds, query):
    pct = dict()
    pct["query"] = 100 * qtds[query] / qtds["pesquisadas"]
    pct["abs"] = 100 * qtds.get("absolutorias", 0) / qtds[query] if pct["query"] != 0 else 0
    pct["con"] = 100 * qtds.get("condenatorias", 0) / qtds[query] if pct["query"] != 0 else 0
    return pct


def corpus_search(D, query, juizos):
    qtds = dict()
    tipos = ["absolutorias", "condenatorias"]
    for juizo in juizos:
        for tipo in tipos:
            qtds[tipo] = 0
            for sentenca in D[juizo][tipo].sentencas:
                if sentenca.find_query(query):
                    qtds[tipo] += 1
    qtds["pesquisadas"] = sum([total_varas(D, juizos, tipo) for tipo in tipos])
    qtds[query] = qtds.get("absolutorias", 0) + qtds.get("condenatorias", 0)
    return qtds


def main():

    query = input("Busca: ")
    juizos = validate_vara(input("Vara: ").split())

    if len(juizos) == 0:
        print("Nenhuma das varas pesquisadas foi encontrada em nosso banco.")
        sys.exit()


    print("Carregando dados...")
    D = load_files(f"./{sys.argv[1]}", juizos)
    numero_sentencas = total_sentencas(D)
    print(f"Dados carregados! Foram carregadas {numero_sentencas} sentenças.")


    qtds = corpus_search(D, query, juizos)
    pct = calc_pcts(qtds, query)

    output = (
        f"Foram pesquisadas {qtds['pesquisadas']} sentenças ",
        f"e o termo {query} foi encontrado em {qtds[query]} delas ",
        f"({pct['query']:.2f}%).\n",
        f"Das {qtds[query]} sentenças encontradas, ",
        f"{qtds.get('absolutorias', 0)} eram absolutorias ({pct['abs']:.2f}%) e ",
        f"{qtds.get('condenatorias', 0)} eram condenatorias ({pct['con']:.2f}%)."
    )

    print("".join(output))


if __name__ == "__main__":
    main()
