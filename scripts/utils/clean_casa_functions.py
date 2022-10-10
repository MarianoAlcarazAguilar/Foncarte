# -*- coding: utf-8 -*-
def clean_casa_sub(s:str):
    '''
    Simplifica el nombre de la casa y lo sustituye con la lista de casas creada
    
    Aguttes, Bloomsbury Auctions, Boisgirard, Bukowskis, De Baecque & Associates,
    Est-Ouest Auctions, Hindman, 'Il Ponte Auction House, Via Pitteri', 
    Metayer, Morton Auctions, Osenat, Stephan Welz & Co.
    '''
    casas_subasta=['33 Auction','Azur','Bonhams','Bruun Rasmussen','Cambi Auction House','Christie\'s','Cornette de Saint Cyr',
                   'DVC','Dreweatts','Fine Art Auctions','Heffel','Ketterer Kunst','Koller','Lyon & Turnbull','Phillips',
                  'Pierre Bergé & Associates','Sotheby\'s', 'Aguttes', 'Bloomsbury Auctions', 
                  'Boisgirard', 'Bukowskis', 'De Baecque & Associates',
                  'Est-Ouest Auctions', 'Hindman', 'Il Ponte Auction House, Via Pitteri', 
                  'Metayer', 'Morton Auctions, Osenat, Stephan Welz & Co.']
    
    for casa in casas_subasta:
        if casa in s:
            s =casa
        
    return s


