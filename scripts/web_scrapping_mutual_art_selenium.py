#! /Users/mariano/anaconda3/bin/python

import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Abrimos los códigos de las nacionalidades latinoamericanas
nacionalidades = pd.read_csv('../datasets/xpathsPaises.csv', header=None)
paises = nacionalidades[0].values
nacionalidades = nacionalidades[1].values


driver = webdriver.Chrome('/usr/local/bin/chromedriver')
driver.maximize_window()

driver.get('https://www.mutualart.com/')

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, 'Log In'))).click()

email = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'login_email')))
password = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'login_passw')))

email.send_keys('jmarinms@hotmail.com')
password.send_keys('Foncarte19')
password.send_keys(Keys.RETURN)

time.sleep(4)
# Entramos en las auctions
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, 'Auctions'))).click()
# Elegimos
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[8]/div[1]/div/nav/ul/li[3]/a'))).click()
# Elegimos subastas que ya se hayan concretado (por el momento lo he deshabilitado)
# WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[8]/div[2]/div/div/div[1]/div/div/div[2]/div[2]/div[1]/div[1]/div/div/div[2]/div/ul/li[1]/label/span[2]'))).click()
# Elegimos solo artistas latinoamericanos
for pais, nacionalidad in zip(paises, nacionalidades):
    time.sleep(3)
    print(pais)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, nacionalidad))).click()

for i in range(100000):
    time.sleep(5)
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    if i % 10 == 0:
        print(f'Guardando html tras {i} búsquedas')
        html = driver.page_source
        with open('../datasets/source_code_mutual_art.html', 'w') as f:
            f.write(html)

driver.quit()
