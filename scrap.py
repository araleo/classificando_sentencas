import re
import string

import bs4
import requests

EXCEPTS = (
    requests.exceptions.ReadTimeout,
    requests.exceptions.SSLError,
    requests.exceptions.ConnectTimeout,
    requests.exceptions.ConnectionError,
    requests.exceptions.TooManyRedirects
)

ERROS = []


def get_request(url):
    try:
        res = requests.get(url)
        res.raise_for_status()
    except EXCEPTS as err:
        ERROS.append(str(err))
        return False
    else:
        return res


def cnj_strip(cnj):
    return "".join([x for x in list(cnj) if x not in string.punctuation])


def main():
    vara = "r1"
    for pg in range(20):
        print(pg)
        busca = f"https://www5.tjmg.jus.br/jurisprudencia/sentenca.do?numeroProcesso=&complemento=&acordaoEmenta=&palavrasConsulta=crime&tipoFiltro=and&relator=&codigoCompostoRelator=&dataInicial=&dataFinal=&numeroUnico=&codigoComarca=231&codigoOrgaoJulgador=231-98-1&resultPagina=50&pg={pg}&pesquisar=Pesquisar"
        res = get_request(busca)
        if res:
            soup = bs4.BeautifulSoup(res.text, "html.parser")
            links = soup.select("#tabelaSentenca img")
            numeros = soup.select(".caixa_processo")
            codigos = []
            cnjs = []
            re8 = re.compile(r"(\d){8}|(\d){7}")
            re32 = re.compile(r"(\w){32}")
            recnj = re.compile(r"\d{7}-\d{2}.\d{4}.\d.\d{2}.\d{4}")

            for link, numero in zip(links, numeros):
                try:
                    codigos.append((re8.search(str(link)).group(), re32.search(str(link)).group()))
                    cnjs.append(cnj_strip(recnj.search(str(numero)).group()))
                except AttributeError as err:
                    ERROS.append(str(err))

            if len(codigos) != len(cnjs):
                ERROS.append(f"numeros incompativeis - {pg}")
            else:
                for cod, cnj in zip(codigos, cnjs):
                    cod8, cod32 = cod
                    dl = f"https://www5.tjmg.jus.br/jurisprudencia/downloadArquivo.do?sistemaOrigem=1&codigoArquivo={cod8}&hashArquivo={cod32}"
                    res = get_request(dl)
                    if res:
                        soup = bs4.BeautifulSoup(res.text, "html.parser")
                        sentenca = soup.get_text()
                        with open(f"./scrap/{vara}/{cnj}{cod8}{cod32}.txt", "w") as f:
                            f.write(sentenca)

    with open(f"./scrap/errorlog.txt", "a") as f:
        for err in ERROS:
            f.write(err)
            f.write("\n")


if __name__ == "__main__":
    main()
