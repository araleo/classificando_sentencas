""" Módulo de funções utilitárias. """

import os


def load_category(cat):
    if cat == "0":
        return "neutras"
    elif cat == "1":
        return "absolutorias"
    elif cat == "2":
        return "condenatorias"
    else:
        return None


def make_folder(path):
    try:
        os.makedirs(path)
    except FileExistsError:
        pass


def set_outfolder(f_class, out, folder):
    if f_class is None:
        outfolder = f"{out}/{folder}/3"
    else:
        outfolder = f"{out}/{folder}/{str(f_class)}"
    make_folder(outfolder)
    return outfolder


def write_outfile(filepath, conteudo):
    with open(filepath, "w") as f:
        f.write(conteudo)
