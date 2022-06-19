import sys
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import time
from settings import ID, PASSWORD

BASE_DIR = os.path.dirname(__file__)
DRIVER_PATH = os.path.join(BASE_DIR, '..','chromedriver')
driver = webdriver.Chrome(DRIVER_PATH)


DATE = '0622'
RESERVATION_TARGET = {'1' : {11, 12}}
# RESERVATION_TARGET = {'1' : {11, 12, 13}, '2': {11, 12, 13}, '3': {11, 12, 13}}
# 11: 1600~1700
# 12: 1700~1800
# 13: 1800~1900


def sendKeys(xpath, keys):
        error = False
        while error == False:
            try:
                driver.find_element(by=By.XPATH, value=xpath).send_keys(keys)
                error = True
            except:
                pass


def click_xPath(xpath):
    error = False
    while error == False:
        try:
            driver.find_element(by=By.XPATH, value=xpath).click()
            error = True
        except:
            C = 1
            print(f'{C}click {xpath}...')
            C += 1
            pass
        

def clickElement(target):
    error = False
    while error == False:
        try:
            target.click()
            error = True
        except:
            pass


def close_alert():
    error=False
    while error==False:
        try:
            driver.switch_to.alert.accept()
            error = True
        except:
            pass
            
            
def findElement(xpath):
    error = False
    while error == False:
        try:
            driver.find_element(by=By.XPATH, value=xpath)
            error = True
        except:
            pass

            
driver.set_window_size(1300, 800)
driver.get('https://www.jungnangimc.or.kr/mem/login')

'''로그인 시작'''
sendKeys('/html/body/div[2]/div[2]/div/div/div/div/ul/li[1]/form/ul/li[1]/ul/li[1]/input', ID)
sendKeys('/html/body/div[2]/div[2]/div/div/div/div/ul/li[1]/form/ul/li[1]/ul/li[2]/input', PASSWORD)
click_xPath('/html/body/div[2]/div[2]/div/div/div/div/ul/li[1]/form/ul/li[2]/input')

# 팝업창 발생 시 닫기
popups = len(driver.window_handles) - 1 
if popups:
    for i in range(popups):
        driver.switch_to.window(driver.window_handles[1])
        driver.close()
    driver.switch_to.window(driver.window_handles[0])
input('Enter! : ')
'''로그인 종료'''

'''Date 입력'''
month = DATE[:2]
day = DATE[2:]


'''링크 타고 들어가서 날짜 누르고 시간대 선택해주기'''
driver.get(f'https://www.jungnangimc.or.kr/rent/date/?yy=2022&mm={month}&q=11/0')
dateBoxes = driver.find_elements(by=By.CLASS_NAME, value='btn_green1')
targetDateBox = None
for dateBox in dateBoxes:
    if dateBox.get_attribute('onclick') == f"getRent('2022{DATE}','11');":
        targetDateBox = dateBox
        break        
clickElement(targetDateBox)



for court in RESERVATION_TARGET:
    for t in RESERVATION_TARGET[court]:
        click_xPath(f'//*[@id="data_tab{court}"]/div[{t}]/label/input')

click_xPath('//*[@id=" "]')
close_alert()


time.sleep(1000)


