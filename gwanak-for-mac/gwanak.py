import sys
import os
from PyQt6.QtWidgets import QMainWindow, QApplication, QInputDialog, QMessageBox, QLineEdit
from PyQt6.QtCore import QDate, QEventLoop, QTimer
from PyQt6 import uic
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
import datetime
import platform
from settings import KEY_URL
from selenium.webdriver.common.keys import Keys

BASE_DIR = os.path.dirname(__file__)
CURRENT_MONTH = str(datetime.datetime.now().month)

if platform.system() == 'Darwin':
    DRIVER_PATH = os.path.join(BASE_DIR, 'chromedriver')
else:
    DRIVER_PATH = os.path.join(BASE_DIR, 'chromedriver.exe')
    
    
class MyApp(QMainWindow, uic.loadUiType(os.path.join(BASE_DIR, 'gwanak.ui'))[0]):
    
    def __init__(self):
        super().__init__()
        self.IS_LOGGED_IN = False
        self.validationKey = self.getValidationKey()
        self.driver = webdriver.Chrome(DRIVER_PATH)
        self.driver.set_window_size(1300, 800)
        self.driver.get('https://www.gwanakgongdan.or.kr/fmcs/126')
        self.setupUi(self)
        self.userPwInputBox.setEchoMode(QLineEdit.EchoMode.Password)
        self.dateInputBox_1.setDate(QDate.currentDate())
        self.dateInputBox_2.setDate(QDate.currentDate())
        self.courtNumSpinBox_1.setRange(1,4)
        self.courtNumSpinBox_2.setRange(1,4)
        self.initUI()
        
    
    ''' 보조 함수들 '''
    def sendKeys(self, xpath, keys):
        error = False
        while error == False:
            try:
                self.driver.find_element(by=By.XPATH, value=xpath).send_keys(keys)
                error = True
            except:
                pass


    def click_xPath(self, xpath):
        error = False
        while error == False:
            try:
                self.driver.find_element(by=By.XPATH, value=xpath).click()
                error = True
            except:
                pass


    def close_alert(self):
        error=False
        while error==False:
            try:
                self.driver.switch_to.alert.accept()
                error = True
            except:
                pass
            
    def findElement(self, xpath):
        error = False
        while error == False:
            try:
                self.driver.find_element(by=By.XPATH, value=xpath)
                error = True
            except:
                pass
                
                
    def sleep(self, x): 
        loop = QEventLoop() 
        x = int(x*1000) 
        QTimer.singleShot(x, loop.quit) 
        loop.exec()
        
    
    def test(self): # 개발할 때 테스트용 함수
        selectedTimes = []
        for i in range(7, 9):
            for j in range(1, 17):
                if self.__dict__[f'day1_{i}_{j}'].isChecked():
                    selectedTimes.append(f'day1_{i}_{j}')
        
    
    def login(self):
        if not self.IS_LOGGED_IN:
            self.userId = self.userIdInputBox.text()
            self.userPw = self.userPwInputBox.text()
            self.sendKeys('//*[@id="user_id"]', self.userId)
            self.sendKeys('//*[@id="user_password"]', self.userPw)
            self.click_xPath('//*[@id="memberLoginForm"]/fieldset/div[2]/span/button')
            
            self.IS_LOGGED_IN = True
            
            self.sleep(2)   # 팝업 창 발생하는지 대기            
            self.closePopUp()
    
    
    def closePopUp(self):
        popups = len(self.driver.window_handles) - 1 
        if popups:
            for _ in range(popups):
                self.driver.switch_to.window(self.driver.window_handles[1])
                self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
            
            
    def reservationDate1(self):
        ''' Date 1 예약 '''
        selectedTimes = []    # 체크한 시간대들을 리스트에 삽입
        
        for i in range(1, 17):
            if self.__dict__[f'time{i}_day1'].isChecked():
                selectedTimes.append(i)

            
        if not selectedTimes:   # 아무 시간대도 체크하지 않았으면 리턴
            return    
        
        date = self.dateInputBox_1.date()
        year = date.year()
        month = date.month()
        month = str(month) if month >= 10 else '0' + str(month)
        day = date.day()
        day = day if day >= 10 else '0' + str(day)
        date = f'{year}{month}{day}'
        courtNum = 284 + self.courtNumSpinBox_1.value()
        
        # 예약 사이트 이동 - 날짜, 코트번호 자동선택됨
        self.driver.get(f'https://www.gwanakgongdan.or.kr/fmcs/116?facilities_type=C&base_date={date}&center=KWAN_AK03&type=1002&part=02&place={courtNum}')
        
        for i in selectedTimes:
            self.click_xPath(f'//*[@id="contents"]/div/div/div/div[3]/div[2]/div/table/tbody/tr[{i}]/td[2]')
        
        self.sendKeys('//*[@id="contents"]/div/div/div/div[4]/button', Keys.ENTER)
        self.findElement('//*[@id="team_nm"]')
        self.sendKeys('//*[@id="team_nm"]', self.driver.find_element(by=By.XPATH, value='//*[@id="mem_nm"]').get_attribute('value'))
        self.sendKeys('//*[@id="users"]', '4')
        self.sendKeys('//*[@id="title"]', '테니스')
        self.sendKeys('//*[@id="purpose"]', '7047')
        self.click_xPath('//*[@id="agree_use1"]')

            
        if not self.testModeBtn.isChecked():
            self.click_xPath('//*[@id="writeForm"]/fieldset/p[2]/button') # 최종 예약신청 버튼
        ''' Date1 예약 종료'''
    
    
    def reservationDate2(self):
        ''' Date 2 예약 '''
        selectedTimes = []    # 체크한 시간대들을 리스트에 삽입
        
        for i in range(1, 17):
            if self.__dict__[f'time{i}_day2'].isChecked():
                selectedTimes.append(i)

        if not selectedTimes:   # 아무 시간대도 체크하지 않았으면 리턴
            return   
        
        date = self.dateInputBox_2.date()
        year = date.year()
        month = date.month()
        month = str(month) if month >= 10 else '0' + str(month)
        day = date.day()
        day = day if day >= 10 else '0' + str(day)
        date = f'{year}{month}{day}'
        courtNum = 284 + self.courtNumSpinBox_2.value()
        
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[1])
        # 예약 사이트 이동 - 날짜, 코트번호 자동선택됨
        self.driver.get(f'https://www.gwanakgongdan.or.kr/fmcs/116?facilities_type=C&base_date={date}&center=KWAN_AK03&type=1002&part=02&place={courtNum}')
        
        for i in selectedTimes:
            self.click_xPath(f'//*[@id="contents"]/div/div/div/div[3]/div[2]/div/table/tbody/tr[{i}]/td[2]')
        
        
        self.sendKeys('//*[@id="contents"]/div/div/div/div[4]/button', Keys.ENTER)
        self.findElement('//*[@id="team_nm"]')
        self.sendKeys('//*[@id="team_nm"]', self.driver.find_element(by=By.XPATH, value='//*[@id="mem_nm"]').get_attribute('value'))
        self.sendKeys('//*[@id="users"]', '4')
        self.sendKeys('//*[@id="title"]', '테니스')
        self.sendKeys('//*[@id="purpose"]', '7047')
        self.click_xPath('//*[@id="agree_use1"]')

            
        if not self.testModeBtn.isChecked():
            self.click_xPath('//*[@id="writeForm"]/fieldset/p[2]/button') # 최종 예약신청 버튼
        ''' Date2 예약 종료'''
    
    def reservationStart(self):
        self.reservationDate1()
        self.reservationDate2()
    
    
    def validationCheck(self):
        key, ok = QInputDialog.getText(self, '사용 허가 키 확인', 'Enter your key: ', QLineEdit.EchoMode.Password)
        
        if not ok: # 취소 버튼을 눌렀을 경우
            sys.exit()
        
        else:   # 확인버튼을 눌렀을 경우 
            if key == self.validationKey:    # 키가 일치할 경우
                return True
            else:   # 키가 일치 하지 않을 경우
                errorMsg = QMessageBox(self)
                errorMsg.setWindowTitle('키 불일치')
                errorMsg.setText('키가 일치하지 않습니다. 개발자에게 문의해 주세요.')
                errorMsg.setStandardButtons(QMessageBox.StandardButton.Yes)
                errorMsg.exec()
                return self.validationCheck()
        
    
    def getValidationKey(self):
        link = requests.get(KEY_URL)
        link_html = BeautifulSoup(link.text, 'html.parser')

        return link_html.select('#mArticle > div.area_view > div > p')[0].text

    
    ''' 메인 함수 '''
    def initUI(self):
        if self.validationCheck():
            self.loginBtn.clicked.connect(self.login)
            self.startBtn.clicked.connect(self.reservationStart)
        else:
            sys.exit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec())