from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup

# browser = webdriver.Chrome('../chromedriver')
# browser.get('https://play.google.com/store/movies/top')


url = 'https://play.google.com/store/movies/top'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36',
    'Accept-Language': 'ko-KR,ko'
}
res = requests.get(url, headers = headers)
res.raise_for_status()
soup = BeautifulSoup(res.text, 'lxml')

movies = soup.find_all('div', attrs={'class': 'ImZGtf mpg5gc'})
print(len(movies))

with open('movi.html', 'w', encoding='utf8') as f:
    f.write(soup.prettify())

for movie in movies:
    title = movie.find('div', attrs = {'class':"WsMG1c nnK0zc"})
    print(title.get_text())

