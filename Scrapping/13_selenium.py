from selenium import webdriver
from selenium.webdriver.common.keys import Keys

browser = webdriver.Chrome('../chromedriver')
browser.get('http://naver.com')

elem = browser.find_element_by_class_name('link_login')
elem.click()

browser.back()
browser.forward()
browser.refresh()
browser.back()

elem = browser.find_element_by_id('query')
elem.send_keys("나도코딩")
elem.send_keys(Keys.ENTER)

elem = browser.find_elements_by_tag_name('a')
for e in elem:
    print(e.get_attribute('href'))



browser.quit()