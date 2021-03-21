""" Módulo para remover acentos dos textos de todos os arquivos. """


import os

from unidecode import unidecode

from util import make_folder


def dir_remover(infolder, outfolder):
    for file in os.listdir(infolder):
        with open(f"{infolder}/{file}", "r") as f:
            conteudo = f.read()
            clean = unidecode(conteudo)
            out = "".join([x.lower() for x in clean])
            out = " ".join(out.split())
            make_folder(outfolder)
            with open(f"{outfolder}/{file[:20]}.txt", "w") as g:
                g.write(out)


def main():
    c_path = "../corpora/corpus"
    for vara in os.listdir(c_path):
        print(vara)
        for cat in os.listdir(f"{c_path}/{vara}"):
            dir_remover(f"{c_path}/{vara}/{cat}", f"./corpora/decoded/{vara}/{cat}")


if __name__ == "__main__":
    main()
