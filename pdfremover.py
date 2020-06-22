import os

def find_pdfs():
    pdfs = []
    for folder in os.listdir("./scrap"):
        for sent in os.listdir(f"./scrap/{folder}"):
            with open(f"./scrap/{folder}/{sent}", "r") as f:
                conteudo = f.read()
                if conteudo.startswith("%PDF"):
                    pdfs.append(f"./scrap/{folder}/{sent}")
    return pdfs


def find_empty():
    e = []
    for folder in os.listdir("./scrap"):
        for sent in os.listdir(f"./scrap/{folder}"):
            with open(f"./scrap/{folder}/{sent}", "r") as f:
                conteudo = f.read()
                if len(conteudo) == 0:
                    e.append(f"./scrap/{folder}/{sent}")
    return e


def remove_bads(bad_files):
    removed = 0
    for bad in bad_files:
        os.remove(bad)
        removed += 1
    return removed


def main():
    e_files = find_empty()
    p_files = find_pdfs()
    print(len(e_files), len(p_files))
    # print(remove_bads(bad_files))


if __name__ == "__main__":
    main()
