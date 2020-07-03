import os

import psycopg2

from google import load_category


def load_texto(filepath):
    with open(filepath, "r") as f:
        conteudo = f.read()
        return conteudo


def main():
    conn = psycopg2.connect("host=192.168.0.100 user=pi dbname=jurimetria")
    cur = conn.cursor()

    root = "./LSVC/corpora"
    corpus = f"{root}/corpus"
    d_corpus = f"{root}/decoded"

    # for vara in os.listdir(corpus):
    vara = "6"
    for cat in os.listdir(f"{corpus}/{vara}"):
        for sent in os.listdir(f"{corpus}/{vara}/{cat}"):
            numero = sent[:20]
            texto = load_texto(f"{corpus}/{vara}/{cat}/{sent}")
            decoded = load_texto(f"{d_corpus}/{vara}/{cat}/{sent[:20]}.txt")
            tipo = load_category(cat)
            cur.execute(
                "INSERT INTO sentencas (vara, numero, texto, decoded, tipo) VALUES (%s, %s, %s, %s, %s)",
                (vara, numero, texto, decoded, tipo)
            )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
