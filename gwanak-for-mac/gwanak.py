
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
from selenium.webdriver.support import expected_conditions as EC

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
    
    
    def click_xPath_if_enable(self, xpath, date):
        error = False
        
        while error == False:
            try:
                date_box = self.driver.find_element(by=By.XPATH, value=f'//*[@id="date-{date}"]')
                
                if date_box.get_attribute("data-state_cd") == "20":
                    self.driver.refresh()   # 새로고침
                    raise Exception("이 날짜는 아직 예약이 안열림. 새로고침 시도")
                self.driver.execute_script("arguments[0].click()", self.driver.find_element(by=By.XPATH, value=xpath))
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
            
            
    def isRsvEnableCheckBy(self, xpath):   # 대관신청버튼을 눌렀을떄 다음페이지로 넘어가졌는가 체크하는 함수
        error = False
        while error == False:
            try:
                self.driver.find_element(by=By.XPATH, value=xpath)
                error = True
            except: # 다음 페이지로 못넘어가서 여기 에러발생, 여기에서 alert 뜨지 않았는지 확인
                if EC.alert_is_present():
                    self.close_alert()
                    return False
                pass
        return True
    
    
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
    
    
    def reserve(self):
        for n in [1,2]:
            checkedAtLeastOneTime = False
            
            if n != 1: # 새 탭 열기
                self.driver.execute_script("window.open('');")
                self.driver.switch_to.window(self.driver.window_handles[n-1])
            
            selectedTimes = []    # 체크한 시간대들을 리스트에 삽입
            
            for i in range(0, 16):
                if self.__dict__[f'time{i}_day{n}'].isChecked():
                    selectedTimes.append(i)

                
            if not selectedTimes:   # 아무 시간대도 체크하지 않았으면 리턴
                return    
            
            date = self.__dict__[f'dateInputBox_{n}'].date()
            year = date.year()
            month = date.month()
            month = str(month) if month >= 10 else '0' + str(month)
            day = date.day()
            day = day if day >= 10 else '0' + str(day)
            date = f'{year}{month}{day}'
            courtNum = 284 + self.__dict__[f'courtNumSpinBox_{n}'].value()
            
            # 예약 사이트 이동 - 날짜, 코트번호 자동선택됨
            self.driver.get(f'https://www.gwanakgongdan.or.kr/fmcs/116?facilities_type=C&base_date={date}&center=KWAN_AK03&type=1002&part=02&place={courtNum}')
            
            
            for i in selectedTimes:
                self.click_xPath_if_enable(f'//*[@id="checkbox_time_{i}"]', date)
                if not checkedAtLeastOneTime and not self.driver.find_element(by=By.XPATH, value=f'//*[@id="checkbox_time_{i}"]').get_attribute('disabled'):
                    checkedAtLeastOneTime = True  # 해당 시간에 예약이 가능해서 한 시간대라도 체크를 했는가?
            
            #하지만 이미 다 예약을 해서 아무것도 체크를 하지 못했다면? 다음으로 못넘어가서 두번째 예약도 못함.
            #실패를 했다면? continue
            if not checkedAtLeastOneTime:
                continue
            
            self.sendKeys('//*[@id="contents"]/div/div/div/div[5]/button', Keys.ENTER)  # 대관신청 버튼
            
            self.findElement('//*[@id="team_nm"]')
            self.sendKeys('//*[@id="team_nm"]', self.driver.find_element(by=By.XPATH, value='//*[@id="mem_nm"]').get_attribute('value'))
            self.sendKeys('//*[@id="users"]', '4')
            self.sendKeys('//*[@id="title"]', '테니스')
            self.sendKeys('//*[@id="purpose"]', '7047')
            self.click_xPath('//*[@id="agree_use1"]')

                
            if not self.testModeBtn.isChecked():
                self.click_xPath('//*[@id="writeForm"]/fieldset/p[2]/button') # 최종 예약신청 버튼
        
    
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
    
    
    def reservationStart(self):
        self.reserve();
    

    
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