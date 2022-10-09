# -*- coding: utf-8 -*-
import pandas as pd
import utils.clean_dim_functions as dim_funcs

def get_sold(df):
    
    sold = df[df['precio_venta'].str.contains('upcoming') == False]
    sold = sold[sold['precio_venta'].str.contains('live now') == False]
    sold = sold[sold['precio_venta'].str.contains('results coming soon') == False]
    sold = sold[sold['precio_venta'].str.contains('not sold') == False]
    
    return sold

def clean_dimensiones(df):
    '''
    Limpia la columna dimensiones y agrega las columnas de height y width
    '''
    df['dimensiones'] = df.dimensiones.apply(lambda x: dim_funcs.fraction_char_replace(x))
    df['dimensiones'] = df.dimensiones.apply(lambda x: dim_funcs.fraction_str_replace(x))
    df['is_inch'] = df.dimensiones.apply(lambda x: dim_funcs.is_inches(x))
    df = dim_funcs.extract_numbers(df)
    
    return df

def clean_autor(df):
    '''
    Limpiar artistas de mutual art y los modifica para
    ser iguales a la lista de artistas acordada
    
    Es probable que se tenga que modificar esta función para añadir nombres adicionales.
    Hay artistas que no son de la lista
    
    SUGERENCIA: quitarle los guiones a todos los nombres (de la tabla de referencia)
    '''
    df['autor'] = df['autor'].str.replace('cesar villacres', 'cesar a.villacres')
    df['autor'] = df['autor'].str.replace('emiliano di cavalcanti', 'emiliano de cavalvanti')
    df['autor'] = df['autor'].str.replace('graciela rodo-boulanger', 'graciela rodo boulanger')
    df['autor'] = df['autor'].str.replace('jesus-rafael soto', 'jesus rafael soto')
    df['autor'] = df['autor'].str.replace('joaquin torres garcia', 'joaquin torres-garcia')
    df['autor'] = df['autor'].str.replace('ignacio iturria', 'ignacio de iturria')
    df['autor'] = df['autor'].str.replace('jose maria mijares', 'jose mijares')
    df['autor'] = df['autor'].str.replace('emiliano di cavalcanti', 'emiliano de cavalvanti')
    df['autor'] = df['autor'].str.replace('ricardo martinez de hoyos', 'ricardo martinez')
        
    return df
