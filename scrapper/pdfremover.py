""" Módulo para remover arquivos .pdf e arquivos vazios baixados pelo scrapper. """


import os


def find_pdfs(path):
    pdfs = []
    for sent in os.listdir(path):
        with open(f"{path}/{sent}", "r") as f:
            conteudo = f.read()
            if conteudo.startswith("%PDF"):
                pdfs.append(f"{path}/{sent}")
    return pdfs


def find_empty(path):
    e = []
    for sent in os.listdir(path):
        with open(f"{path}/{sent}", "r") as f:
            conteudo = f.read()
            if len(conteudo) == 0:
                e.append(f"{path}/{sent}")
    return e


def remove_bads(bad_files):
    removed = 0
    for bad in bad_files:
        os.remove(bad)
        removed += 1
    return removed


def main():
    e_files = find_empty("../tributario/raw")
    p_files = find_pdfs("../tributario/raw")
    print(len(e_files), len(p_files))
    print(remove_bads(e_files + p_files))


if __name__ == "__main__":
    main()
