""" Módulo para classificação humana de sentenças utilizando o terminal. """


import os

from util import load_category, write_outfile


root = f"./scrapper/t3"

def main():
    for i, sent in enumerate(os.listdir(root)):
        with open(f"{root}/{sent}", "r") as f:
            if i < 78:
                continue
            conteudo = f.read()
            if "contribuição à saúde no percentual de 3,2" not in conteudo and "restituírem à parte autora os valores descontados a título de contribuição à saúde" not in conteudo:
                print(conteudo)
                print(i)
                categoria = load_category(input("Categoria: "))
                if categoria is not None:
                    write_outfile(f"./tributario/labels/{categoria}/{sent}", conteudo)


if __name__ == "__main__":
    main()
