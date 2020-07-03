import os


LISTA_FEITAS = ["1", "3", "4", "5", "6", "7", "8", "9", "10", "11", "b1", "b2", "b3"]
root = f"./TSC2/corpus"


def check_ans(resposta):
    if resposta == "0":
        return "neutras"
    elif resposta == "1":
        return "absolutorias"
    elif resposta == "2":
        return "condenatorias"
    elif resposta == "3":
        return None


def write_file(cat, nome, conteudo):
    with open(f"./TSC2/human/{cat}/{nome}", "w") as f:
        f.write(conteudo)
        print(f"Salva na categoria {cat} - {nome}")


def main():
    # for vara in os.listdir(root):
    vara = "t2"
    for cat in os.listdir(f"{root}/{vara}"):
        if cat == "3" or cat == "4":
            for file in os.listdir(f"{root}/{vara}/{cat}"):
                with open(f"{root}/{vara}/{cat}/{file}", "r") as f:
                    conteudo = f.read()
                    print(conteudo)
                    categoria = check_ans(input("Categoria: "))
                    if categoria is not None:
                        write_file(categoria, file, conteudo)


if __name__ == "__main__":
    main()