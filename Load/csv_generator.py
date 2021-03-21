import sys

from unidecode import unidecode

from TextSearch.google import corpus_search, load_files, total_sentencas, total_varas


tipos = ["absolutorias", "condenatorias", "neutras"]
varas = ["1", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "t1", "t2", "t3"]
indexes = ["vara", "total", "sonegacao", "lavagem", "corrupcao", "furto", "roubo", "homicidio", "trafico", "estelionato", "desacato", "estupro", "latrocinio"]

def load_querys():
    return [
        "Sonegação",
        "Lavagem dinheiro",
        "Corrupção",
        "Furto",
        "Roubo",
        "Homicídio",
        "Tráfico",
        "Estelionato",
        "Desacato",
        "Estupro",
        "Latrocínio"
    ]


def expand_index(id):
    return f"{id}_abs,{id}_con,{id}_neu"


def first_line():
    return ",".join([idx if idx == "vara" else expand_index(idx) for idx in indexes])


def write_outfile(linhas):
    fpath = "./sentencas.csv"
    with open(fpath, "w") as f:
        f.write(linhas)


def load_data():
    print("Carregando dados...")
    d = load_files(f"./{sys.argv[1]}")
    print(f"Dados carregados! Foram carregadas {total_sentencas(d)} sentenças.")
    return d


def csv_generator():
    querys = load_querys()
    d = load_data()
    linhas = first_line()
    for vara in varas:
        totais = {tipo: total_varas(d, [vara], tipo) for tipo in tipos}
        linhas += f"\n{vara},"
        linhas += f"{totais['absolutorias']},{totais['condenatorias']},{totais['neutras']}"
        for query in querys:
            query = unidecode(query.lower())
            _, qtds = corpus_search(d, query, [vara], tipos)
            linhas += f",{qtds['absolutorias']},{qtds['condenatorias']},{qtds['neutras']}"
    write_outfile(linhas)
    # print(linhas)

def main():
    csv_generator()
    pass


if __name__ == "__main__":
    main()
