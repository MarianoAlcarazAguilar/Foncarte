# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from calendar import month_abbr

import utils.clean_dim_functions as dim_funcs
import utils.clean_casa_functions as casa_funcs

def get_sold(df):
    '''
    sold = df[df['precio_venta'].str.contains('upcoming', case =False) == False]
    sold = sold[sold['precio_venta'].str.contains('live now', case =False) == False]
    sold = sold[sold['precio_venta'].str.contains('results coming soon', case =False) == False]
    sold = sold[sold['precio_venta'].str.contains('not sold', case =False) == False]
    '''
    
    sold = df[df.precio_venta != 0]

    return sold

def clean_date(df_orig):
    '''
    Cambia el formato a YYYY-MM-DD
    '''
    lower_ma = [m.lower() for m in month_abbr]
    df = df_orig.copy()
    #BORRAR LUEGO
    df['fecha'] = df['fecha'].str.lower()
    
    months = df['fecha'].str.extract('([a-z]{3})')
    months = months[0].str.lower().map(lambda m: lower_ma.index(m)).astype('Int8')
    years = df['fecha'].str.extract('([0-9]{4})')
    days = df['fecha'].str.extract('([0-9]{2}),')

    df['fecha'] = years[0]+'-'+months.astype(str)+'-'+days[0]
    df['fecha'] = pd.to_datetime(df['fecha'])
    
    return df

def clean_fecha_creac(df):
    '''
    PUEDEN SALIR VALORES MAYORES A 2022
    AGREGAR QUE LA FECHA DE CREAC SEA MENOR A LA DE VENTA

    '''
    
    df['fecha_creacion'] = df['fecha_creacion'].str.extract('([0-9]{4})')
    #quitar si se puede
    df = df[df['fecha_creacion'].isna() == False]
    df['fecha_creacion'] = pd.to_numeric(df['fecha_creacion'])
    df = df[df['fecha_creacion'] <= 2022]
    
    return df

def clean_dimensiones(df):
    '''
    Limpia la columna dimensiones y agrega las columnas de height y width
    '''
    df['dimensiones'] = df.dimensiones.apply(lambda x: dim_funcs.fraction_char_replace(x))
    df['dimensiones'] = df.dimensiones.apply(lambda x: dim_funcs.fraction_str_replace(x))
    df['is_inch'] = df.dimensiones.apply(lambda x: dim_funcs.is_inches(x))
    df = dim_funcs.extract_numbers(df)
    
    df = df[df['is_inch'] != -1]
    
    return df

def clean_autor(df):
    '''
    Limpiar artistas de mutual art y los modifica para
    ser iguales a la lista de artistas acordada
    
    Es probable que se tenga que modificar esta funci??n para a??adir nombres adicionales.
    Hay artistas que no son de la lista
    
    SUGERENCIA: quitarle los guiones a todos los nombres (de la tabla de referencia)
    '''
    df['autor'] = df['autor'].str.replace('cesar villacres', 'cesar a. villacres')
    df['autor'] = df['autor'].str.replace('emiliano di cavalcanti', 'emiliano de cavalcanti')
    df['autor'] = df['autor'].str.replace('graciela rodo-boulanger', 'graciela rodo boulanger')
    df['autor'] = df['autor'].str.replace('jesus-rafael soto', 'jesus rafael soto')
    df['autor'] = df['autor'].str.replace('joaquin torres garcia', 'joaquin torres-garcia')
    df['autor'] = df['autor'].str.replace('ignacio iturria', 'ignacio de iturria')
    df['autor'] = df['autor'].str.replace('jose maria mijares', 'jose mijares')
    df['autor'] = df['autor'].str.replace('leopoldo romanac', 'leopoldo romanach')
    df['autor'] = df['autor'].str.replace('ricardo martinez de hoyos', 'ricardo martinez')
        
    return df

def clean_casa(df):
    '''
    aplica la funcion que limpia la columna casa_subasta
    '''
    df['casa_subasta'] = df['casa_subasta'] = df['casa_subasta'].apply(lambda x: casa_funcs.clean_casa_sub(x))
    
    return df


def to_lower(df):
  columnsTolower = list(df.select_dtypes(include=['category','object']))
  for feature in columnsTolower:
      try:
          df[feature] = df[feature].str.lower()
      except:
          print('Error parsing '+feature)
  return df


def clean_precios(df):
    '''
    convierte la columna precio ajustado a valores num??ricos
    '''
    df['precio_ajustado'] = df['precio_ajustado'].str.replace(',','')
    df['precio_ajustado'] = df['precio_ajustado'].str.replace(' USD','')
    df['precio_ajustado'] = pd.to_numeric(df['precio_ajustado'])
    
    return df

def clean_titulo(df):
    df['titulo'] = df['titulo'].str.split(' by ').str[0]
    
    return df

def calc_performance(df):
    '''
    DF despu??s de haber limpiado los precios

    Parameters
    ----------
    df : TYPE
        DESCRIPTION.

    Returns
    -------
    df_test : TYPE
        DESCRIPTION.

    df_test = df
    
    df_test['precio_estimado'] = df_test['precio_estimado'].str.replace(',','')
    df_test['lower'] = df_test['precio_estimado'].str.extract('([0-9][0-9]?[0-9]?[0-9]?[0-9]?[0-9]?[0-9]?)')
    df_test['precio_estimado'] = df_test['precio_estimado'].str.replace('[0-9][0-9]?[0-9]?[0-9]?[0-9]?[0-9]?[0-9]?','', n=1)
    df_test['upper'] = df_test['precio_estimado'].str.extract('([0-9][0-9]?[0-9]?[0-9]?[0-9]?[0-9]?[0-9]?)')
    df_test['upper'] = np.where(df_test['upper'].isna(), (df_test['lower'].astype(int)), df_test['upper'])
    df_test['avg'] = (df_test['lower'].astype(int) + df_test['upper'].astype(int))/2
    df_test['performance'] = df_test['precio_ajustado']/df_test['avg']
    '''


    df['lst_precio_estimado'] = df['precio_estimado'].str.split(' ')
    df['avg'] = df['lst_precio_estimado'].apply(lambda x: (float(x[0])+float(x[2]))/2 if x[0]!='nan' else 'NA')
    df['performance'] = df['precio_ajustado']/df['avg']
    
    return df
    

def clean_mutual_art(df):
    '''
    Limpiar la tabla de mutual art

    '''
    df = get_sold(df)
    df = clean_date(df)
    df = clean_dimensiones(df)
    df = clean_autor(df)
    df = clean_casa(df)
    df = clean_fecha_creac(df)
    #df = clean_precios(df)
    df = clean_titulo(df)
    df = calc_performance(df)
    
    
    return df

def standardize_data(df):
    df = clean_mutual_art(df)
    
    #faltar??a: performance, source y country
    df['age'] = 2022-df['fecha_creacion']
    df['source'] = 'Mutual Art'
    df['country'] = '-'
    
    df = df[['titulo', 'height', 'width', 'tipo', 'tecnica', 'fecha_creacion',
             'age','casa_subasta', 'fecha', 'precio_ajustado', 'autor', 'performance',
             'source','country']]
    
    df.rename(columns={'titulo':'title','width':'length', 'tipo':'art_type', 'tecnica':'medium_text', 
                       'fecha_creacion':'date_text', 'casa_subasta': 'house',
                       'precio_ajustado': 'price', 'autor': 'author'}, inplace=True)
    
    #a titulo quitarle by ...
    #renombrar columnas
    #precio como valor num??rico # arreglar las cosas de los n??meros
    #sacar promedio del precio estimado
    #ajustar performance con monedas ( over si ya est?? en d??lares)
    #a??adir col de pa??s de origen
    
    # ----
    df = to_lower(df)

    return df



df = pd.read_csv('/Users/guillermonaranjomuedano/Documents/Escuela/Materias Antiguas/7?? Semestre/To??pico de Negocios II/Proyecto Foncarte/Foncarte/datasets/data_mutualart_completo_ajustado.csv')
#df = clean_mutual_art(df)
df = standardize_data(df)

df.head(10)

df.to_csv('/Users/guillermonaranjomuedano/Documents/Escuela/Materias Antiguas/7?? Semestre/To??pico de Negocios II/Proyecto Foncarte/Foncarte/datasets/clean/clean_mut_art_ver2_ajustado.csv')



#TO-DO
# de fecha creacion ver que onda con los valores no num??ricos
# simplificar m??s casa de subasta
#simplificar tecnica - in progress
#aplicar esto para toodooos los datos que tenemos y quitar duplicados
