import requests


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36'
}

url = 'http://nadocoding.tistory.com'

res = requests.get(url=url, headers=headers)
with open('nadocoding.html', 'w', encoding='utf-8') as f:
    f.write(res.text)
