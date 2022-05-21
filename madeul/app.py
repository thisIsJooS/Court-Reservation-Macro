import sys
import pathlib
from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtCore import QDate, QEventLoop, QTimer
from PyQt6 import uic
from selenium import webdriver
from selenium.webdriver.common.by import By


class MyApp(QMainWindow, uic.loadUiType('madeul.ui')[0]):
    
    def __init__(self):
        super().__init__()
        self.driver = webdriver.Chrome(f'{pathlib.Path(__file__).parent.parent.resolve()}/chromedriver')
        self.driver.set_window_size(1200, 800)
        self.driver.get('https://reservation.nowonsc.kr/member/login')
        self.setupUi(self)
        self.date1InputBox.setDate(QDate.currentDate())
        self.date2InputBox.setDate(QDate.currentDate())
        self.date3InputBox.setDate(QDate.currentDate())
        self.date4InputBox.setDate(QDate.currentDate())
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
        

    def test(self):
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
        
        self.sleep(2)
        print(len(self.driver.window_handles))
        if len(self.driver.window_handles) != 1:   # 팝업창 발생 시 
            self.driver.switch_to.window(self.driver.window_handles[1])
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
    
    
    def reservationDate1(self):
        ''' Date 1 예약 '''
        selectedTimes = []    # 체크한 시간대들을 리스트에 삽입
        for i in range(7, 9):
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
        date1_month = date1_month if date1_month >= 10 else '0' + str(date1_month)
        date1_day = self.date1.day()
        date1_day = date1_day if date1_day >= 10 else '0' + str(date1_day)
        
        self.driver.get('https://reservation.nowonsc.kr/sports/tennis_list')
        self.click_xPath('//*[@id="container"]/div[2]/div[2]/div[1]/div[2]/div[2]/a[2]') # 대관신청 버튼
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
        for i in range(7, 9):
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
        date2_month = date2_month if date2_month >= 10 else '0' + str(date2_month)
        date2_day = self.date2.day()
        date2_day = date2_day if date2_day >= 10 else '0' + str(date2_day)
        
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.get('https://reservation.nowonsc.kr/sports/tennis_list')
        self.click_xPath('//*[@id="container"]/div[2]/div[2]/div[1]/div[2]/div[2]/a[2]') # 대관신청 버튼
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
        for i in range(7, 9):
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
        date3_month = date3_month if date3_month >= 10 else '0' + str(date3_month)
        date3_day = self.date3.day()
        date3_day = date3_day if date3_day >= 10 else '0' + str(date3_day)
        
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[2])
        self.driver.get('https://reservation.nowonsc.kr/sports/tennis_list')
        self.click_xPath('//*[@id="container"]/div[2]/div[2]/div[1]/div[2]/div[2]/a[2]') # 대관신청 버튼
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
    
    
    def reservationDate4(self):
        ''' Date 4 예약 '''
        selectedTimes = []    # 체크한 시간대들을 리스트에 삽입
        for i in range(7, 9):
            isFull = False
            for j in range(1, 17):
                if self.__dict__[f'day4_{i}_{j}'].isChecked():
                    selectedTimes.append((i, j))
                
                if len(selectedTimes) >= 4: 
                    isFull = True
                    break
            
            if isFull: break
        
        if not selectedTimes:   # 아무 시간대도 체크하지 않았으면 리턴
            return
        
        self.date4 = self.date4InputBox.date()
        date4_year = self.date4.year()
        date4_month = self.date4.month()
        date4_month = date4_month if date4_month >= 10 else '0' + str(date4_month)
        date4_day = self.date4.day()
        date4_day = date4_day if date4_day >= 10 else '0' + str(date4_day)
        
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[3])
        self.driver.get('https://reservation.nowonsc.kr/sports/tennis_list')
        self.click_xPath('//*[@id="container"]/div[2]/div[2]/div[1]/div[2]/div[2]/a[2]') # 대관신청 버튼
        self.click_xPath('//*[@id="frm"]/div/div[1]/div/div/div/div[3]/span') # 다음달 넘어가기
        
        self.click_xPath(f'//*[@id="td-{date4_year}-{date4_month}-{date4_day}"]') # 날짜 선택
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
        ''' Date 4 예약 종료'''
    
    
    def reservationStart(self):
        self.reservationDate1()
        self.reservationDate2()
        self.reservationDate3()
        self.reservationDate4()
    
    
    ''' 메인 함수 '''
    def initUI(self):
        self.loginBtn.clicked.connect(self.login)
        self.startBtn.clicked.connect(self.reservationStart)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec())