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


