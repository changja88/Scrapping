import requests


if __name__ == '__main__':
    res = requests.get('http://google.com')

    if res.status_code == requests.codes.ok:
        print("200 OK")

    res.raise_for_status()  # 오류 나면 프로그램 종료
    print('웹 스크래핑 진행합니다')


    with open("mygoogle.html", "w", encoding='utf-8') as f:
        f.write(res.text)