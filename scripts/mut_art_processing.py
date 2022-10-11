# -*- coding: utf-8 -*-
import pandas as pd
from calendar import month_abbr

import utils.clean_dim_functions as dim_funcs
import utils.clean_casa_functions as casa_funcs

def get_sold(df):
    
    sold = df[df['precio_venta'].str.contains('upcoming', case =False) == False]
    sold = sold[sold['precio_venta'].str.contains('live now', case =False) == False]
    sold = sold[sold['precio_venta'].str.contains('results coming soon', case =False) == False]
    sold = sold[sold['precio_venta'].str.contains('not sold', case =False) == False]
    
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
    
    Es probable que se tenga que modificar esta función para añadir nombres adicionales.
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

def clean_precios(df):
    '''
    convierte la columna precio ajustado a valores numéricos
    '''
    df['precio_ajustado'] = df['precio_ajustado'].str.replace(',','')
    df['precio_ajustado'] = df['precio_ajustado'].str.replace(' USD','')
    df['precio_ajustado'] = pd.to_numeric(df['precio_ajustado'])
    
    return df

def clean_titulo(df):
    df['titulo'] = df['titulo'].str.split(' by ').str[0]
    
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
    df = clean_precios(df)
    df = clean_titulo(df)
    
    
    return df

def standardize_data(df):
    df = clean_mutual_art(df)
    
    #faltaría: performance, source y country
    df['age'] = 2022-df['fecha_creacion']
    df['source'] = 'Mutual Art'
    df['country'] = '-'
    df['performance'] = -420
    
    df = df[['titulo', 'height', 'width', 'tipo', 'tecnica', 'fecha_creacion',
             'age','casa_subasta', 'fecha', 'precio_ajustado', 'autor', 'performance',
             'source', 'country']]
    
    df.rename(columns={'titulo':'title','width':'length', 'tipo':'art_type', 'tecnica':'medium_text', 
                       'fecha_creacion':'date_text', 'casa_subasta': 'house',
                       'precio_ajustado': 'price', 'autor': 'author'}, inplace=True)
    
    #a titulo quitarle by ...
    #renombrar columnas
    #precio como valor numérico # arreglar las cosas de los números
    #sacar promedio del precio estimado
    #calcular performance
    #añadir col de país de origen
    
    # ----

    return df



df = pd.read_csv('../datasets/data_mutualart_completo.csv')
#df = clean_mutual_art(df)
df = standardize_data(df)

#df.to_csv('../datasets/clean/clean_mut_art_ver2.csv')



#TO-DO
# de fecha creacion ver que onda con los valores no numéricos
# simplificar más casa de subasta
#simplificar tecnica - in progress
#aplicar esto para toodooos los datos que tenemos y quitar duplicados
