from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys

browser = webdriver.Chrome('../chromedriver')
browser.get('http://naver.com')

elem = browser.find_element_by_class_name('link_login')
elem.click()

browser.find_element_by_id('id').send_keys('changja0329')
time.sleep(1)
browser.find_element_by_id('pw').send_keys('Djdnls88!!')
time.sleep(2)

browser.find_element_by_id('log.login').click()


time.sleep(5)
browser.quit()