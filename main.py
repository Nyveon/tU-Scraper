from secrets import cookie
from bs4 import BeautifulSoup
from cursos import Ramo
import requests
import json

# Setup
catalogo = "fcfm_catalogo"
semestre = 20221
depto = 5

# Request and parse
URL = f"https://ucampus.uchile.cl/m/{catalogo}/?semestre={semestre}&depto={depto}"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

# Processing
ramos = []
soup_ramos = soup.find_all("div", class_="ramo")
for soup_ramo in soup_ramos:
    ramos.append(Ramo(soup_ramo))

print(ramos)
for ramo in ramos:
    print(ramo.to_json())