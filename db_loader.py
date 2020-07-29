import os

import psycopg2

from util import load_category


def load_texto(filepath):
    with open(filepath, "r") as f:
        conteudo = f.read()
        return conteudo


def main():
    conn = psycopg2.connect("dbname=dfc67a8iipaeqb user=jisxbmuyjgymou password=54d9e761006413376160f41e9b858661b6f11f95ccf2897723f41d1e1ba7be77 host=ec2-34-239-241-25.compute-1.amazonaws.com port=5432")
    cur = conn.cursor()

    lista_varas = ["11", "12"]

    root = "./corpora"
    corpus = f"{root}/corpus"
    d_corpus = f"{root}/decoded"

    for vara in lista_varas:
        print(vara)
        for cat in os.listdir(f"{corpus}/{vara}"):
            tipo = load_category(cat)
            if tipo:
                for sent in os.listdir(f"{corpus}/{vara}/{cat}"):
                    numero = sent[:20]
                    texto = load_texto(f"{corpus}/{vara}/{cat}/{sent}")
                    decoded = load_texto(f"{d_corpus}/{vara}/{cat}/{sent[:20]}.txt")
                    tribunal = "TJMG"

                    try:
                        cur.execute(
                            "INSERT INTO jurimetria_sentenca (tribunal, vara, numero, texto, decoded, tipo) VALUES (%s, %s, %s, %s, %s, %s)",
                            (tribunal, vara, numero, texto, decoded, tipo)
                        )
                    except psycopg2.Error as e:
                        print(numero, e)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
