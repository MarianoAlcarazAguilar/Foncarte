# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import re

import unicodedata

def fraction_char_replace(s):
    '''
    Reemplaza las fracciones representadas como un solo caracter y las convierte en decimales
    ej: ¾, ½ se convierten en .75 y .5
    Args: 
        s(str)- string de las dimensiones de una obra
    '''
    
    for c in s:
        try:
            name = unicodedata.name(c)
        except ValueError:
            continue
        if name.startswith('VULGAR FRACTION'):
            normalized = unicodedata.normalize('NFKC', c)
            numerator, _slash, denominator = normalized.partition('⁄')
            
            frac = int(numerator)/int(denominator)
            s = s.replace(c, str(frac))
            #yield c, numerator, denominator
            
    return s

def fraction_str_replace(s):
    '''
    Se asume que dentro de cada registro, se encuentra un 
    Formas de detectat una fraccion de la forma a/b:
    
    num a/b
    
    aaa/b
    
    num-a/b
    
    num.a/b
    
    ojo: existe .groups()
    '''
    if(re.search(' [0-9]?[0-9]/[0-9]?[0-9]', s)):  #tipo num a/b
        
        #es un ciclo porque se debe de tratar cada fraccion en todo el string
        for m in re.findall('([0-9]?[0-9])/([0-9]?[0-9])',s): #lista de tuplas para cada fracción
            num, denom = int(m[0]), int(m[1])
            frac = num/denom
            frac = re.sub('0','',str(frac))
            
            pattern = ' '+str(num)+'/'+str(denom)
            
            s = re.sub(pattern, frac,s)
        
    elif(re.search('[0-9][0-9]{2}?/[0-9][0-9]?',s)): #tipo aaa/b
        
        for m in re.findall('([0-9][0-9][0-9])/([0-9][0-9]?)',s): #lista de tuplas para cada fracción
            num, denom = int(m[0]), int(m[1])
            frac = num/denom
            pattern = str(num)+'/'+str(denom)
            
            s = re.sub(pattern, str(frac),s)
        
    elif(re.search('[0-9][0-9]?-[0-9][0-9]?/[0-9]?[0-9]',s)):
        #tipo num-a/b
        
        for m in re.findall('([0-9][0-9]?[0-9]?)/([0-9][0-9]?)',s): #lista de tuplas para cada fracción
            num, denom = int(m[0]), int(m[1])
            frac = num/denom
            frac = re.sub('0','',str(frac))
            pattern = '-'+str(num)+'/'+str(denom)
            
            s = re.sub(pattern, frac,s)
        
    elif(re.search('[0-9]\.[0-9][0-9]?/[0-9]?[0-9]',s)):
        #tipo num.a/b
        
        for m in re.findall('([0-9][0-9]?[0-9]?)/([0-9][0-9]?)',s): #lista de tuplas para cada fracción
            num, denom = int(m[0]), int(m[1])
            frac = num/denom
            frac = re.sub('0\.','',str(frac))
            pattern = str(num)+'/'+str(denom)
            
            s = re.sub(pattern, frac,s)
        
    else: 
        resp = 'no se detectó'
    
    return s

def is_inches(s):
    '''
    
    '''
    no_measures_ids = ['various sizes', 'dimensions variable', 'property from the estate of bernard chappard\xa0 ...']
    inches_ids = ['in', '"', '\'\'', '″',  'a']
    cm_ids = ['cm', 'mm', 'm']
    
    if any(keyword in s for keyword in inches_ids):
        is_inch = 1
    elif any(keyword in s for keyword in cm_ids):
        is_inch = 0
    elif any(keyword in s for keyword in no_measures_ids):
        is_inch = -1
    else: 
        is_inch = 1 #if no imformation is given of it's measurements, it is assumed that the measures are in inches
        #is_inch = 2 #in case if a problem is detected and some rows need to be flagged
    
    return is_inch

def extract_numbers(df):
    '''
    Se extrae los primeros 2 valores numéricos que se encuentre y se pasan cm si son pulgadas. Se asumen 3 cosas:
    
    - que no hay obras de 3 dimensiones (esculturas, etc...)
    - si vienen las medidas 2 veces, primero se observan las pulgadas
    - 
    '''
    df['height'] = df.dimensiones.str.extract('([0-9][0-9]?[0-9]?\.?[0-9]?[0-9]?[0-9]?)') #normalmente se extrae el primer match
    temp_series = df.dimensiones.str.replace('[0-9][0-9]?[0-9]?\.?[0-9]?[0-9]?[0-9]?', '',regex=True, n=1)
    df['height'] = pd.to_numeric(df['height'])
    df['width'] = temp_series.str.extract('([0-9][0-9]?[0-9]?\.?[0-9]?[0-9]?[0-9]?)')
    df['width'] = pd.to_numeric(df['width'])
    
    return df


