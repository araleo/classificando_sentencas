""" Módulo para classificação humana de sentenças utilizando o terminal. """


import os

from Util.util import load_category
from Util.util import write_outfile


root = f"../Data/corpora/jfrj"
outfolder = f"../Data/labels"


def main():
    for i, sent in enumerate(os.listdir(root)):
        with open(f"{root}/{sent}", "r") as f:
            conteudo = f.read()
            print(conteudo)
            print(i)
            categoria = load_category(input("Categoria: "))
            if categoria is not None:
                write_outfile(f"{outfolder}/{categoria}/{sent}", conteudo)


if __name__ == "__main__":
    main()
