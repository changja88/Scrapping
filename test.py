import requests
from bs4 import BeautifulSoup


header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36',
    'Cookie': 'SSOTOKENYN=Y; EHTcCode=0000000800; WMONID=VP5vCzcZo6U; EHReferCode=800; _fbp=fb.1.1612856896861.407339552; _ga=GA1.2.1888631357.1612856898; _gid=GA1.2.1122422466.1612856898; checkAdPup=done; EHCustNO=D9PrYXQWHdm%2BykYaouc%2BGw%3D%3D; ENCEHCustNO=70044ad24d8af3dddc75a4a6443602bc; GGimCnt=0; EHCartSize=0; MyAmt=0%7C0%7C7001%7C13625; _TRK_IS_COOKIE=_TRK_MBR%3DY%5E_TRK_ISLOGIN%3DY%5E_TRK_AG%3DZ%5E_TRK_UVP1%3DD%5E_TRK_UVP2%3DHPOINT; RECENT_VIEW_SHPG=%7B%22rcntShpg%22%3A%5B%22item%242109511488%24150496%22%5D%7D; RECENT_VIEW_ITEMS=H2109511488%2F2109511488_0_100.jpg%2F150496%2FN; NEW_JSESSIONID=B8SF9OG4_CU5ZmLT96N2v_Kbbe-zCNUwJByS3UOUbf_PCRLbAYvl!-997433439; _TRK_ICO={"viewItems":[]}; wcs_bt=s_5117770cb5ce:1612863166; pageMoveCnt=24; _INSIGHT_CK_901=6ba21e1c09cd4114a3827f438f01ebe2_56897|37674812e57011d272f011fc7c405505_63147:1612864966000'
}
url = 'https://www.hmall.com/p/mpa/selectOrdPTCPup.do?ordNo=20210204320814'
res = requests.get(url, headers=header)

soup = BeautifulSoup(res.text, 'lxml')
buttons = soup.find_all('div', attrs={'class': 'btngroup'})

for button in buttons:
    if button.get_text() == '배송조회':
        print('abc')
    else:
        print(button.get_text())


# 361349650750
# //*[@id="mainContents"]/div/div/div[2]/div/div[1]/dl/dd/div
