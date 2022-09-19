#! /Users/mariano/anaconda3/bin/python

'''
Primero sacamos todos los nombres de las obras usando url_general
RECORDAR que hay múltiples páginas
link base: https://www.madart.com.mx/es/galeria?pag=
Al final se agrega el número. Va del 0 al 37

En cada obra dentro de la div.obra_item viene un atributo que se llama onclick de la siguiente forma:
    onclick="window.location='obra-retrato-7'"
Necesitamos extraer el obra-retrato-7

link base obra: https://www.madart.com.mx/es/
Al final se agrega lo extraído en el paso anterior

De ese html extraemos la div.obra_info
Y ya ahí está everything
'''

from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests
import re

# GENERALES
url_general = "https://www.madart.com.mx/es/galeria?pag="

# OUTPUTS
obras_link_ref = []

for url_i in range(38):
    url_aux = f'{url_general}{url_i}'
    print(url_aux)

    result = requests.get(url_aux).text
    doc = BeautifulSoup(result, "html.parser")

    obras = doc.find_all(class_='obra_item')
    for obra in obras:
        on_click_text = obra.attrs['onclick']
        obra_link_ref = re.split(r'\'', on_click_text)[1]
        obras_link_ref.append(obra_link_ref)

# Convertimos la lista en un np.array
obras_link_ref = np.array(obras_link_ref)
# Pasamos los datos a un data frame para poderlos guardar en un csv
pd.DataFrame(obras_link_ref).to_csv('../datasets/obras_names_links.csv', index=False, header=False)
print(f'obras encontradas: {obras_link_ref.size}')
