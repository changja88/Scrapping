import requests
from bs4 import BeautifulSoup
import re

url = 'https://www.coupang.com/np/search?q=%EB%85%B8%ED%8A%B8%EB%B6%81&channel=user&component=&eventCategory=SRP&trcid=&traid=&sorter=scoreDesc&minPrice=&maxPrice=&priceRange=&filterType=&listSize=36&filter=&isPriceRange=false&brand=&offerCondition=&rating=0&page=2&rocketAll=false&searchIndexingToken=1=4&backgroundColor='
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36'
}
res = requests.get(url, headers = headers)
soup = BeautifulSoup(res.text, 'lxml')

items = soup.find_all('li', attrs={'class': re.compile('^search-product')})
for item in items:

    ad_badge = item.find('span', attrs={'class': 'ad-badge_text'})
    if ad_badge:
        print('광고 제외')
        continue

    name = item.find('div', attrs ={'class': 'name'}).get_text()
    price = item.find('strong', attrs ={'class': 'price-value'}).get_text()
    rate = item.find('em', attrs ={'class': 'rating'})
    if rate:
        rate = rate.get_text()
    else:
        rate = '평점 없음'

    count = item.find('span', attrs ={'class': 'rating-total-count'})
    if rate:
        count = count.get_text()
    else:
        count = '평점 없음'

    print(name)
    print(price)
    print(rate)
    print(count)



