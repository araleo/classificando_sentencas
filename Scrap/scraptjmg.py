""" Módulo de webscraping da página do TJMG. """


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
    """Recebe uma url e retorna um request"""
    try:
        res = requests.get(url)
        res.raise_for_status()
    except EXCEPTS as err:
        ERROS.append(str(err))
        return False
    else:
        return res


def cnj_strip(cnj):
    """Recebe uma string e retorna sem pontuação"""
    return "".join([x for x in list(cnj) if x not in string.punctuation])


def get_lista_datas(datas):
    """Recebe um objeto bs4 e retorna uma lista com strings das datas naquele objeto """
    re_data = re.compile(r"\d\d/\d\d/\d\d\d\d")
    lista_datas = []
    for data in datas:
        x = re_data.search(str(data))
        if x:
            group = x.group()
            stripped = "".join([c for c in group if c not in string.punctuation])
            lista_datas.append(stripped)
    return lista_datas


def main():
    vara = "aluguel"
    for pg in range(5):
        print(pg)
        busca = f"https://www5.tjmg.jus.br/jurisprudencia/sentenca.do?numeroProcesso=&complemento=&acordaoEmenta=&palavrasConsulta=aluguel+residencial+rescis%E3o+contratual+locat%E1rio+multa&tipoFiltro=and&relator=&codigoCompostoRelator=&dataInicial=&dataFinal=&codigoComarca=24&codigoOrgaoJulgador=&resultPagina=50&pg={pg}&pesquisar=Pesquisar"
        res = get_request(busca)
        if res:
            soup = bs4.BeautifulSoup(res.text, "html.parser")
            links = soup.select("#tabelaSentenca img")
            numeros = soup.select(".caixa_processo")
            datas_soup = soup.select(".corpo")
            codigos = []
            cnjs = []
            datas = get_lista_datas(datas_soup)
            re8 = re.compile(r"(\d){8}|(\d){7}|(\d){6}")
            re32 = re.compile(r"(\w){32}")
            recnj = re.compile(r"\d{7}-\d{2}.\d{4}.\d.\d{2}.\d{4}")

            for link, numero in zip(links, numeros):
                try:
                    codigos.append((re8.search(str(link)).group(), re32.search(str(link)).group()))
                    cnjs.append(cnj_strip(recnj.search(str(numero)).group()))
                except AttributeError as err:
                    ERROS.append(str(err))

            if len(codigos) != len(cnjs) or len(codigos) != len(datas):
                ERROS.append(f"numeros incompativeis - {pg}")
            else:
                for cod, cnj, data in zip(codigos, cnjs, datas):
                    cod8, cod32 = cod
                    dl = f"https://www5.tjmg.jus.br/jurisprudencia/downloadArquivo.do?sistemaOrigem=1&codigoArquivo={cod8}&hashArquivo={cod32}"
                    res = get_request(dl)
                    if res:
                        soup = bs4.BeautifulSoup(res.text, "html.parser")
                        sentenca = soup.get_text()
                        with open(f"./{vara}/{cnj}{data}{cod8}.txt", "w") as f:
                            f.write(sentenca)

    with open(f"errorlog.txt", "a") as f:
        for err in ERROS:
            f.write(err)
            f.write("\n")


if __name__ == "__main__":
    main()
