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

BASE_DIR = os.path.dirname(__file__)
CURRENT_MONTH = str(datetime.datetime.now().month)

class MyApp(QMainWindow, uic.loadUiType(os.path.join(BASE_DIR, 'madeul.ui'))[0]):
    
    def __init__(self):
        super().__init__()
        self.validationKey = self.getValidationKey()
        self.driver = webdriver.Chrome(os.path.join(BASE_DIR, 'chromedriver'))
        self.driver.set_window_size(1200, 800)
        self.driver.get('https://reservation.nowonsc.kr/member/login')
        self.setupUi(self)
        self.userPwInputBox.setEchoMode(QLineEdit.EchoMode.Password)
        self.date1InputBox.setDate(QDate.currentDate())
        self.date2InputBox.setDate(QDate.currentDate())
        self.date3InputBox.setDate(QDate.currentDate())
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
        self.userId = self.userIdInputBox.text()
        self.userPw = self.userPwInputBox.text()
        self.sendKeys('//*[@id="memberId"]', self.userId)
        self.sendKeys('//*[@id="memberPassword"]', self.userPw)
        self.click_xPath('//*[@id="frm"]/fieldset/div/div[4]/button')
        
        self.sleep(2)   # 팝업 창 발생하는지 대기
        if len(self.driver.window_handles) != 1:   # 팝업창 발생 시 팝업 끄고 메인 윈도우로 이동
            self.driver.switch_to.window(self.driver.window_handles[1])
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
    
    
    def reservationDate1(self):
        ''' Date 1 예약 '''
        selectedTimes = []    # 체크한 시간대들을 리스트에 삽입
        for i in range(7, 10):
            isFull = False
            for j in range(1, 17):
                if self.__dict__[f'day1_{i}_{j}'].isChecked():
                    selectedTimes.append((i, j))
                
                if len(selectedTimes) >= 4: 
                    isFull = True
                    break
            
            if isFull: break
            
        if not selectedTimes:   # 아무 시간대도 체크하지 않았으면 리턴
            return    
        
        self.date1 = self.date1InputBox.date()
        date1_year = self.date1.year()
        date1_month = self.date1.month()
        date1_month = str(date1_month) if date1_month >= 10 else '0' + str(date1_month)
        date1_day = self.date1.day()
        date1_day = date1_day if date1_day >= 10 else '0' + str(date1_day)
        
        self.driver.get('https://reservation.nowonsc.kr/sports/tennis_list')
        self.click_xPath('//*[@id="container"]/div[2]/div[2]/div[1]/div[2]/div[2]/a[2]') # 대관신청 버튼
        
        if CURRENT_MONTH != date1_month[-1]: # 예약하고자 하는 달이 다른 달인 경우
            self.click_xPath('//*[@id="frm"]/div/div[1]/div/div/div/div[3]/span') # 다음달 넘어가기
        
        self.click_xPath(f'//*[@id="td-{date1_year}-{date1_month}-{date1_day}"]') # 날짜 선택
        for td, tr in selectedTimes:     # 선택한 시간대들 체크
            self.click_xPath(f'//*[@id="timeBody"]/tr[{tr}]/td[{td*2-1}]/div/label')
        self.click_xPath('//*[@id="reserved_submit"]') # 예약 버튼
        self.close_alert() # 대관신청 dialog 확인
        
        
        try:  # 하나도 예약하지 못했을 경우 _value 값을 불러오지 못해 에러 발생
            captchaValue = self.driver.execute_script('return _value')
        except:
            captchaValue = False
        
        
        if captchaValue:  # 시간대 체크에 성공 했을 경우
            self.sendKeys('//*[@id="value"]', self.driver.execute_script('return _value'))
            self.click_xPath('//*[@id="capt_check"]')
            self.close_alert()
            self.click_xPath('//*[@id="container"]/div[2]/div[2]/div[3]/div/label')
            
            if not self.testModeBtn.isChecked():
                self.click_xPath('//*[@id="frm"]/div/button[1]') # 최종 예약신청 버튼
                self.close_alert()
        ''' Date1 예약 종료'''
    
    
    def reservationDate2(self):
        ''' Date 2 예약 '''
        selectedTimes = []    # 체크한 시간대들을 리스트에 삽입
        for i in range(7, 10):
            isFull = False
            for j in range(1, 17):
                if self.__dict__[f'day2_{i}_{j}'].isChecked():
                    selectedTimes.append((i, j))
                
                if len(selectedTimes) >= 4: 
                    isFull = True
                    break
            
            if isFull: break
        
        if not selectedTimes:   # 아무 시간대도 체크하지 않았으면 리턴
            return
        
        self.date2 = self.date2InputBox.date()
        date2_year = self.date2.year()
        date2_month = self.date2.month()
        date2_month = str(date2_month) if date2_month >= 10 else '0' + str(date2_month)
        date2_day = self.date2.day()
        date2_day = date2_day if date2_day >= 10 else '0' + str(date2_day)
        
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.get('https://reservation.nowonsc.kr/sports/tennis_list')
        self.click_xPath('//*[@id="container"]/div[2]/div[2]/div[1]/div[2]/div[2]/a[2]') # 대관신청 버튼
        
        if CURRENT_MONTH != date2_month[-1]: # 예약하고자 하는 달이 다른 달인 경우
            self.click_xPath('//*[@id="frm"]/div/div[1]/div/div/div/div[3]/span') # 다음달 넘어가기
        
        self.click_xPath(f'//*[@id="td-{date2_year}-{date2_month}-{date2_day}"]') # 날짜 선택
        for td, tr in selectedTimes:     # 선택한 시간대들 체크
            self.click_xPath(f'//*[@id="timeBody"]/tr[{tr}]/td[{td*2-1}]/div/label')
        self.click_xPath('//*[@id="reserved_submit"]') # 예약 버튼
        self.close_alert() # 대관신청 dialog 확인
        
        
        try:  # 하나도 예약하지 못했을 경우 _value 값을 불러오지 못해 에러 발생
            captchaValue = self.driver.execute_script('return _value')
        except:
            captchaValue = False
        

        if captchaValue:  # 시간대 체크에 성공 했을 경우
            self.sendKeys('//*[@id="value"]', self.driver.execute_script('return _value'))
            self.click_xPath('//*[@id="capt_check"]')
            self.close_alert()
            self.click_xPath('//*[@id="container"]/div[2]/div[2]/div[3]/div/label')
            
            if not self.testModeBtn.isChecked():
                self.click_xPath('//*[@id="frm"]/div/button[1]') # 최종 예약신청 버튼
                self.close_alert()
        ''' Date 2 예약 종료'''
    
    
    def reservationDate3(self):
        ''' Date 3 예약 '''
        selectedTimes = []    # 체크한 시간대들을 리스트에 삽입
        for i in range(7, 10):
            isFull = False
            for j in range(1, 17):
                if self.__dict__[f'day3_{i}_{j}'].isChecked():
                    selectedTimes.append((i, j))
                
                if len(selectedTimes) >= 4: 
                    isFull = True
                    break
            
            if isFull: break
        
        if not selectedTimes:   # 아무 시간대도 체크하지 않았으면 리턴
            return
        
        
        self.date3 = self.date3InputBox.date()
        date3_year = self.date3.year()
        date3_month = self.date3.month()
        date3_month = str(date3_month) if date3_month >= 10 else '0' + str(date3_month)
        date3_day = self.date3.day()
        date3_day = date3_day if date3_day >= 10 else '0' + str(date3_day)
        
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[2])
        self.driver.get('https://reservation.nowonsc.kr/sports/tennis_list')
        self.click_xPath('//*[@id="container"]/div[2]/div[2]/div[1]/div[2]/div[2]/a[2]') # 대관신청 버튼
        
        if CURRENT_MONTH != date3_month[-1]: # 예약하고자 하는 달이 다른 달인 경우
            self.click_xPath('//*[@id="frm"]/div/div[1]/div/div/div/div[3]/span') # 다음달 넘어가기
        
        self.click_xPath(f'//*[@id="td-{date3_year}-{date3_month}-{date3_day}"]') # 날짜 선택
        for td, tr in selectedTimes:     # 선택한 시간대들 체크
            self.click_xPath(f'//*[@id="timeBody"]/tr[{tr}]/td[{td*2-1}]/div/label')
        self.click_xPath('//*[@id="reserved_submit"]') # 예약 버튼
        self.close_alert() # 대관신청 dialog 확인
        
        
        try:  # 하나도 예약하지 못했을 경우 _value 값을 불러오지 못해 에러 발생
            captchaValue = self.driver.execute_script('return _value')
        except:
            captchaValue = False
        
        
        if captchaValue:  # 시간대 체크에 성공 했을 경우
            self.sendKeys('//*[@id="value"]', self.driver.execute_script('return _value'))
            self.click_xPath('//*[@id="capt_check"]')
            self.close_alert()
            self.click_xPath('//*[@id="container"]/div[2]/div[2]/div[3]/div/label')
            
            if not self.testModeBtn.isChecked():
                self.click_xPath('//*[@id="frm"]/div/button[1]') # 최종 예약신청 버튼
                self.close_alert()
        ''' Date 3 예약 종료'''
    
    
    def reservationStart(self):
        self.reservationDate1()
        self.reservationDate2()
        self.reservationDate3()
    
    
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
        link = requests.get('https://thisisjoos.tistory.com/257')
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