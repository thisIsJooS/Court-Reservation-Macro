import sys
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import time
from selenium.webdriver.common.keys import Keys
from settings import ID, PASSWORD

BASE_DIR = os.path.dirname(__file__)
DRIVER_PATH = os.path.join(BASE_DIR, '..','chromedriver')
driver = webdriver.Chrome(DRIVER_PATH)

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
        

def refresh_until_open(date):
    error = False
    
    while error == False:
        try:
            date_box = driver.find_element(by=By.XPATH, value=f'//*[@id="date-2022{date}"]')
            
            if date_box.get_attribute("data-state_cd") == "20":
                driver.refresh()   # 새로고침
                raise Exception("이 날짜는 아직 예약이 안열림. 새로고침 시도")
            # driver.execute_script("arguments[0].click()", driver.find_element(by=By.XPATH, value=xpath))
            error = True
        except:
            pass
    


driver.set_window_size(1300, 800)
driver.get('https://www.ycs.or.kr/page/etc/login.php')

'''로그인 시작'''
sendKeys('//*[@id="id"]', ID)
sendKeys('//*[@id="pw"]', PASSWORD)
click_xPath('//*[@id="content"]/form/div/input[3]')

# 팝업창 발생 시 닫기
popups = len(driver.window_handles) - 1 
if popups:
    for _ in range(popups):
        driver.switch_to.window(driver.window_handles[1])
        driver.close()
    driver.switch_to.window(driver.window_handles[0])
'''로그인 종료'''

'''예약 사이트 이동'''

target_date = input("며칠? ex)0920 >> ")
target_court = input("몇번코트? ex)3 >> ")
'''
https://www.ycs.or.kr/yeyak/fmcs/43?facilities_type=C&base_date=20220920&rent_type=1001&center=YCS04&part=02&place=2 #2번코트
https://www.ycs.or.kr/yeyak/fmcs/43?facilities_type=T&base_date=20220920&rent_type=1001&center=YCS04&part=02&place=4 #4번코트
'''
reservation_url = f'https://www.ycs.or.kr/yeyak/fmcs/43?facilities_type=T&base_date=2022{target_date}&rent_type=1001&center=YCS04&part=02&place={target_court}'
driver.get(reservation_url)

'''풀릴떄까지 새로고침'''
'''//*[@id="date-20220927"]'''
refresh_until_open(target_date)



# #미리가서 새로고침하고있어야 하나?
# time.sleep(5)
# print("5초지남")

'''시간대 임의 지정 - 1300~1400(5회), 1400~1500(6회)
1회 : //*[@id="checkbox_time_0"]

5회 : //*[@id="checkbox_time_4"]
//*[@id="contents"]/article/div/div/div[5]/div[2]/div/table/tbody/tr[5]/td[1]
6회 : //*[@id="checkbox_time_5"]
//*[@id="contents"]/article/div/div/div[5]/div[2]/div/table/tbody/tr[6]/td[1]
'''
click_xPath('//*[@id="checkbox_time_4"]')
click_xPath('//*[@id="checkbox_time_5"]')
sendKeys('//*[@id="contents"]/article/div/div/div[6]/button', Keys.ENTER)


findElement('//*[@id="team_nm"]')
sendKeys('//*[@id="team_nm"]', '1')
sendKeys('//*[@id="users"]', '4')
sendKeys('//*[@id="purpose"]', '1')
click_xPath('//*[@id="agree_use1"]')


time.sleep(1000)


