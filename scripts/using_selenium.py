#! /Users/mariano/anaconda3/bin/python

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome('/usr/local/bin/chromedriver')
driver.maximize_window()

driver.get('https://www.mutualart.com/')

# Abrimos la página de login
driver.find_element(By.LINK_TEXT, 'Log In').click()

# Insertamos nuestros datos
time.sleep(3)
driver.find_element(By.ID, 'login_email').send_keys('jmarinms@hotmail.com')
password = driver.find_element(By.ID, 'login_passw')

password.send_keys('Foncarte19')
password.send_keys(Keys.RETURN)

time.sleep(2)
driver.find_element(By.LINK_TEXT, 'Auctions').click()
time.sleep(2)
driver.find_element(By.XPATH, '/html/body/div[8]/div[1]/div/nav/ul/li[3]/a').click()
time.sleep(2)
driver.find_element(By.XPATH, '/html/body/div[8]/div[2]/div/div/div[1]/div/div/div[2]/div[2]/div[1]/div[1]/div/div/div[2]/div/ul/li[1]/label/span[2]').click()

for i in range(10):
    time.sleep(4)
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

html = driver.page_source
with open('../datasets/source_code_mutual_art.html', 'w') as f:
    f.write(html)

driver.quit()