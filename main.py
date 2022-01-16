from secrets import cookie
from bs4 import BeautifulSoup
from cursos import Ramo
import requests
import json



## -- Catalogo de cursos --
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

# Output
ramos_json = []
for ramo in ramos:
    ramos_json.append(ramo.to_json())

with open("ramos.json", "w") as output_file:
    output_file.write(
        json.dumps(
            ramos_json,
            ensure_ascii=False
        )
    )


# todo: recuento de creditos
