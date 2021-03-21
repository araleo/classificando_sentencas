""" Módulo de webscraping da página da JFRJ. """


import requests
from datetime import datetime

from bs4 import BeautifulSoup


DOMAIN = "https://www10.trf2.jus.br/consultas/"


def make_file(path, text):
    with open(path, "w") as f:
        f.write(text)


def main():
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    start = 0
    vara = "9"

    while True:

        if start > 990:
            break

        print(start)

        URL = f"https://www10.trf2.jus.br/consultas/?proxystylesheet=v2_index&getfields=*&entqr=3&lr=lang_pt&ie=UTF-8&oe=UTF-8&requiredfields=(-sin_proces_sigilo_judici:s).(-sin_sigilo_judici:s)&partialfields=DescOrgaoJulgador:0{vara}%C2%AA+VARA+FEDERAL+CRIMINAL+DO+RIO+DE+JANEIRO&sort=date:D:S:d1&entsp=a&adv=1&base=SE&ulang=&access=p&entqrm=0&wc=200&wc_mc=0&ud=1&client=v2_index&filter=0&as_q=&q=&start={start}&site=v2_sentencas"

        res = requests.get(URL, verify=False)
        soup = BeautifulSoup(res.text, "html.parser")
        urls = [u for u in soup.find_all("a") if str(u.get("href")).startswith("?movimento=")]

        for url in urls:
            num = url["title"][-20:]
            now = str(datetime.now().timestamp()).replace(".", "")
            _url = DOMAIN + url["href"]
            res = requests.get(_url, verify=False)
            soup = BeautifulSoup(res.text, "html.parser")
            text = soup.get_text()
            make_file(f"./jfrj/{vara}/{num}{now}.txt", text)

        start += 10


if __name__ == "__main__":
    main()
