import os
import shutil


def abs_e_neutras(root, out):
    for vara in os.listdir(root):
        for cat in os.listdir(f"{root}/{vara}"):
            src = f"{root}/{vara}/{cat}"
            if cat == "0":
                dst = f"{out}/{vara}/0"
                shutil.copytree(src, dst)
            elif cat == "1":
                dst = f"{out}/{vara}/1"
                shutil.copytree(src, dst)
            elif cat == "3":
                dst = f"{out}/{vara}/4"
                shutil.copytree(src, dst)


def move_condenatorias(root, out):
    for vara in os.listdir(root):
        for cat in os.listdir(f"{root}/{vara}"):
            src = f"{root}/{vara}/{cat}"
            if cat == "1":
                dst = f"{out}/{vara}/2"
                shutil.copytree(src, dst)
            elif cat == "3":
                dst = f"{out}/{vara}/3"
                shutil.copytree(src, dst)


def move_nc(root, out):
    for vara in os.listdir(root):
        print(vara)
        for cat in os.listdir(f"{root}/{vara}"):
            src = f"{root}/{vara}/{cat}"
            if cat == "0":
                dst = f"{out}/{vara}"
                shutil.copytree(src, dst)


def main():
    move_condenatorias("./TCTS/classified_c_nc", f"./TCTS/corpus")
    abs_e_neutras("./TCTS/classified_a_n", f"./TCTS/corpus")
    pass


if __name__ == "__main__":
    main()
