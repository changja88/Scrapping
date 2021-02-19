import requests
from bs4 import BeautifulSoup


url = 'https://comic.naver.com/webtoon/weekday.nhn'
res = requests.get(url)
res.raise_for_status()

soup = BeautifulSoup(res.text, 'lxml')
# lxml로 ress.text를 파싱 해서 BeautifulSoup객체로 만듬

print(soup.title)  # html 전부 가져옴
print(soup.title.get_text())  # 내용(글자) 만 가져옴
print(soup.a)  # 처음 발견되는 a 를 가져옴
print(soup.a.attrs)  # 속성을 가져온다 (dict로 가져옴)
print(soup.a['href'])  # 특정 값만을 가져온다

a = soup.find('a', attrs={'class': 'Nbtn_upload'})  # 태그 중에서 class 속성이 Nbtn_upload인걸 찾아온다
a = soup.find(attrs={'class': 'Nbtn_upload'})  # class 속성이 Nbtn_upload인걸 찾아온다
print(a)

rank1 = soup.find('li', attrs={'class': 'rank01'})
print(rank1.a.get_text())
rank2 = rank1.next_sibling.next_sibling  # 중간에 개행 정보가 있으면 두번 해줘야 다음것이 나올 수도 있다
print(rank2.a.get_text())
rank1 = rank2.previous_sibling.previous_sibling
print(rank1.a.get_text())
print(rank1.parent)  # 부모로 이동

rank2 = rank1.find_next_sibling('li')  # 조건에 해당하는 형제만 찾는다
print(rank2.a.get_text())
rank1 = rank2.find_previous_sibling('li')
print(rank1.a.get_text())

rank1.find_next_siblings('li')  # 형제'들'을 가져온다

webtoon = soup.find('a', text='독립일기-62화 눈 온다')
print(webtoon)
