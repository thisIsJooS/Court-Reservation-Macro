from selenium import webdriver

driver = webdriver.Chrome('./chromedriver')

def open():
    driver.get('https://www.naver.com')