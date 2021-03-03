from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

browser = webdriver.Chrome('../chromedriver')
# browser.maximize_window()
browser.get('http://flight.naver.com/flights/')

browser.find_element_by_link_text('가는날 선택').click()

browser.find_elements_by_link_text('27')[0].click()
browser.find_elements_by_link_text('28')[1].click()

browser.find_element_by_xpath("//*[@id='recommendationList']/ul/li[1]").click()

browser.find_element_by_link_text('항공권 검색').click()

# 로딩 처리 하는 방법
# 1 -> 그냥 몇초 기다린다
# 2 -> 라이브러리 쓴다
try:
    elem = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='content']/div[2]/div/div[4]/ul/li[1]"))
    )
    elem = browser.find_element_by_xpath("//*[@id='content']/div[2]/div/div[4]/ul/li[1]")
    print(elem.text)
finally:
    browser.close()
