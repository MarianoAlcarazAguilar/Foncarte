#! /Users/mariano/anaconda3/bin/python

from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests

obras = pd.read_csv('../datasets/obras_names_links.csv', header=None, names=['nombre'])
obras = obras.nombre.values
obras = obras[550:650]
link_base = 'https://www.madart.com.mx/es/'
resultados = np.array(('artista', 'nombre_obra', 'tecnica', 'anio', 'precio', 'altura', 'ancho'))
guardar_datos_parciales = False
# En la primera corrida se guardaron los primeros 600 datos
iteration = 0

for obra in obras:
    # Generamos y llamamos el link de la obra buscada
    link_obra = f'{link_base}{obra}'
    result = requests.get(link_obra).text
    doc = BeautifulSoup(result, "html.parser")

    datos_obra = doc.find(class_='obra_info')

    nombre_obra = datos_obra.find(class_='obra_obra3').text
    print(nombre_obra)
    artista = datos_obra.find(class_='obra_artista').text
    varios = datos_obra.find_all(class_='obra_dato')
    altura = varios[0].text.split()[0]
    ancho = varios[0].text.split()[2]
    tecnica = varios[1].text
    anio = varios[2].text
    precio = int(''.join(datos_obra.find(class_='obra_precio').text.split('$')[1].split(',')))

    datos_limpios = np.array((artista, nombre_obra, tecnica, anio, precio, altura, ancho))
    resultados = np.vstack((resultados, datos_limpios))

    if guardar_datos_parciales:
        iteration += 1
        if iteration % 100 == 0:
            print(f'\n\nGuardando datos: {iteration}\n\n')
            pd.DataFrame(resultados[1:], columns=resultados[0])\
                .to_csv(f'../datasets/datos_obras_parciales_{iteration}.csv', header=True, index=False)

pd.DataFrame(resultados[1:], columns=resultados[0]).to_csv('../datasets/datos_obras.csv', header=True, index=False)
