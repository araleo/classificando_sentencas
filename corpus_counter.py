""" Módulo para exibir a contagem e porcentagem de cada tipo de sentença classificada. """


import os

from util import load_category


def imprime(d):
    total = sum(d.values())
    abs = d["absolutorias"] / total * 100
    con = d["condenatorias"] / total * 100
    neu = d["neutras"] / total * 100
    fal = d["falhas"] / total * 100
    print(f"absolutorias: {d['absolutorias']} - {abs:.2f}% ")
    print(f"condenatorias: {d['condenatorias']} - {con:.2f}% ")
    print(f"neutras: {d['neutras']} - {neu:.2f}% ")
    print(f"falhas: {d['falhas']} - {fal:.2f}%")


def main():
    root = "./corpora/corpus"
    d = {}

    for vara in os.listdir(root):
        d[vara] = {}
        for categoria in os.listdir(f"{root}/{vara}"):
            c = load_category(categoria)
            cat = c if c is not None else "falhas"
            d[vara].setdefault(cat, 0)
            d[vara][cat] += len(os.listdir(f"{root}/{vara}/{categoria}"))

    for k in d:
        print(k)
        imprime(d[k])


if __name__ == "__main__":
    main()
