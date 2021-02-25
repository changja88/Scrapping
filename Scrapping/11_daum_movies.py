import requests
from bs4 import BeautifulSoup
import re


for year in range(2015, 2021):

    url = f'https://search.daum.net/search?nil_suggest=btn&w=tot&DA=SBC&q={year}%EB%85%84%20%EC%98%81%ED%99%94%EC%88%9C%EC%9C%84&spacing=2&orgq=2019%EB%85%84%20%EC%98%81%ED%99%94%EC%88%98%EB%88%84%EC%9D%B4'
    res = requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, 'lxml')
    images = soup.find_all('img', attrs={'class': 'thumb_img'})

    for index, image in enumerate(images):
        image_url = image['src']
        if image_url.startswith('//'):
            image_url = 'https:' + image_url

        image_res = requests.get(image_url)
        image_res.raise_for_status()

        with open(f'movie_{year}_{index + 1}.jpg', 'wb')as f:
            f.write(image_res.content)

        if index >= 4:
            break
