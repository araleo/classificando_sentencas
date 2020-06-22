import os

from unidecode import unidecode

def text_remover(text):
    return (unidecode(text))


def dir_remover():
    for file in os.listdir("./teste"):
        with open(f"./teste/{file}", "r") as f:
            conteudo = f.read()
            clean = unidecode(conteudo)
            with open(f"./teste/clean{file}", "w") as g:
                g.write(clean)


def main():

    with open("./teste/teste2.txt", "r") as f:
        conteudo = f.read()
        clean = unidecode(conteudo).split()
        clean_set = set(unidecode(conteudo).split())

        print(conteudo)
        print(clean)
        print(clean_set)

        while True:
            query = unidecode(input())
            print(query in conteudo)
            print(query in clean)
            print(query in clean_set)



if __name__ == "__main__":
    main()
