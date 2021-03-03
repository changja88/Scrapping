from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup


options = webdriver.ChromeOptions()
options.headless = True
options.add_argument(
    'User-Agent= Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36'
)


browser = webdriver.Chrome('../chromedriver', options=options)
browser.get('https://play.google.com/store/movies/top')
# 해드리스 크롭으로 하면 user-agent에 headlessChrome이 찍힌다 -> 이건 막힐수 있기 때문에 user-agent를 적어 주는게 좋다

# 지정한 위치로 스크롤 내리기
# browser.execute_script("window.scrollTo(0,1440)")  # 1440 으로 스크롤 내리기

# 화면 가장 아래로 스크롤 내리기
# browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')

interval = 2
prev_height = browser.execute_script('return document.body.scrollHeight')

while True:
    browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    time.sleep(interval)  # 페이지로딩 대기
    current_height = browser.execute_script('return document.body.scrollHeight')

    if current_height == prev_height:
        break
    else:
        prev_height = current_height

soup = BeautifulSoup(browser.page_source, 'lxml')
movies = soup.find_all('div', attrs={'class': ['ImZGtf mpg5gc', 'Vpfmgd']})

for movie in movies:
    title = movie.find('div', attrs={'class': "WsMG1c nnK0zc"})
    print(title.get_text())

print('스크린 샷')
browser.get_screenshot_as_file('google_movie.png')

time.sleep(10)
browser.close()
