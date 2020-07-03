import os

def load_category(cat):
    if cat == "0":
        return "neutras"
    elif cat == "1":
        return "absolutorias"
    elif cat == "2":
        return "condenatorias"
    else:
        return "falhas"


def imprime(d):
    total = sum(d.values())
    abs = d["absolutorias"] / total * 100
    con = d["condenatorias"] / total * 100
    neu = d["neutras"] / total * 100
    fal = d["falhas"] / total * 100
    print(f"Absolutorias: {abs:.2f} ")
    print(f"condenatorias: {con:.2f} ")
    print(f"neutras: {neu:.2f} ")
    print(f"falhas: {fal:.2f} ")


def main():
    root = "./TCTS/corpus"
    d = {}

    for vara in os.listdir(root):
        d[vara] = {}
        for cat in os.listdir(f"{root}/{vara}"):
            d[vara].setdefault(load_category(cat), 0)
            d[vara][load_category(cat)] += len(os.listdir(f"{root}/{vara}/{cat}"))

    for k in d:
        print(k)
        imprime(d[k])


if __name__ == "__main__":
    main()