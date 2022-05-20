import sys
from tkinter import Widget
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import requests
from bs4 import BeautifulSoup


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('My First Application')
        self.setWindowIcon(QIcon('web.png'))    # 타이틀바의 아이콘
        self.resize(800, 600)
        self.center() # 창이 화면의 가운데에 위치하게 함
        self.initUI()


    def center(self):
        qr = self.frameGeometry()   # 스크린의 위치와 크기 정보를 가져옴
        cp = QGuiApplication.primaryScreen().availableGeometry().center() # 스크린의 가운데 위치 파악
        qr.moveCenter(cp)   # 창의 직사각형 위치를 화면의 중심의 위치로 이동
        self.move(qr.topLeft()) # 현재 창을 화면의 중심으로 이동했던 직사각형(qr)의 위치로 이동시킴.


    def initUI(self):
        self.btn = QPushButton('버튼', self)
        self.btn.clicked.connect(self.btnEvent)
        
        self.tb = QTextBrowser()
        self.tb.setAcceptRichText(True)
        self.tb.setOpenExternalLinks(True)

        vbox = QVBoxLayout()
        vbox.addWidget(self.btn, 0)
        vbox.addWidget(self.tb, 1)

        self.setLayout(vbox)
        
        
        # Main
        self.show()
    
    
    def btnEvent(self):
        naver_finance = requests.get('https://finance.naver.com/sise/sise_market_sum.naver')
        naver_finance_html = BeautifulSoup(naver_finance.text, 'html.parser')
        corps = naver_finance_html.select('tbody .tltle')

        for i in range(1, len(corps)+1):
            self.tb.append(str(f'{i} : {corps[i-1].text}'))
        
        
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec())