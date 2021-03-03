from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup


browser = webdriver.Chrome('../chromedriver')
browser.get('https://play.google.com/store/movies/top')

# 지정한 위치로 스크롤 내리기
# browser.execute_script("window.scrollTo(0,1440)")  # 1440 으로 스크롤 내리기

# 화면 가장 아래로 스크롤 내리기
# browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')

interval = 2
prev_height = browser.execute_script('return document.body.scrollHeight')

while True:
    browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    time.sleep(interval) # 페이지로딩 대기
    current_height = browser.execute_script('return document.body.scrollHeight')

    if current_height == prev_height:
        break
    else:
        prev_height = current_height

soup = BeautifulSoup(browser.page_source, 'lxml')
movies = soup.find_all('div', attrs={'class': ['ImZGtf mpg5gc','Vpfmgd']})

for movie in movies:
    title = movie.find('div', attrs = {'class':"WsMG1c nnK0zc"})
    print(title.get_text())




time.sleep(10)
browser.close()