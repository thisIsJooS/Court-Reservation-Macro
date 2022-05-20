import requests
from bs4 import BeautifulSoup


naver_finance = requests.get('https://finance.naver.com/sise/sise_market_sum.naver')
naver_finance_html = BeautifulSoup(naver_finance.text, 'html.parser')
corps = naver_finance_html.select('tbody .tltle')

for i in range(1, len(corps)+1):
    print(f'{i} : {corps[i-1].text}')