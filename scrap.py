import os
import requests
import zipfile
from bs4 import BeautifulSoup, SoupStrainer
import re


DOMAIN = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
OUTPUT_DIR = 'pdfs'
ZIP_FILENAME = 'pdfs_files.zip'

#Baixa o arquivo recebendo url e o nome
def get_file(url, file_name):
    # faz requisição ao servidor
    response = requests.get(url)
    if response.status_code == requests.codes.OK:
        with open(file_name, 'wb') as new_file:
            new_file.write(response.content)
        print("Download completed: {}".format(file_name))
    else:
        response.raise_for_status()

#Zipar os arquivos, recebendo o nome do arquivo zip e uma lista dos arquivos baixados
def zip_file(zip_filename, downloaded_files):
    with zipfile.ZipFile(zip_filename, 'w') as zip_file:
        for file in downloaded_files:
            zip_file.write(file, os.path.basename(file))

def main():
    response = requests.get(DOMAIN)
    downloaded_files = []

    if response.status_code == requests.codes.OK:
        #Definir o filtro dos arquivos "Anexos" e analizando o html com filtro
        link_filter = SoupStrainer('a', href=re.compile(r'Anexo.*\.pdf$'))
        links_pdfs = BeautifulSoup(response.text, 'html.parser', parse_only=link_filter)

        #Extrair o nome do arquivo da url
        for link in links_pdfs:
            pdf_url = link.get('href')
            filename = os.path.join(OUTPUT_DIR, os.path.basename(pdf_url))

            get_file(pdf_url, filename)

            downloaded_files.append(filename)

            zip_file(ZIP_FILENAME, downloaded_files)
    else:
        print("Error", response.status_code)



if __name__ == "__main__":
    main()

