import csv
import re
import urllib
from datetime import date

import requests
from bs4 import BeautifulSoup


def make_csv_writer():
    filename = f'../3_Result/{date.today()} 옵션 없는 상품.csv'
    f = open(filename, 'w', encoding='utf-8-sig', newline='')
    writer = csv.writer(f)
    return writer


def get_item_url(item):
    encoded_item = urllib.parse.quote(item)
    url = f'https://www.galleria.co.kr/search/totalSearch.action?searchTerm={encoded_item}&page_idx=&cateLM=&totalFilter=&disp_type_cd_dq=10&mall_no=0000014&cateYn=&searchType=&searchNumCheck=&selectChkYn='
    return url


def get_item_list():
    # 아이템 리스트 내부 한개의 형식
    # [상품번호, 상품명, 판매상테 ,백화점정가, 옵션유무]

    item_list = []
    with open('../1_Row/2021_02_28.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        for row in reader:
            item_list.append([row[0], modify_item_name(row[4]), row[7], row[10], row[17]])

    return item_list


def cleanText(readData):
    # 텍스트에 포함되어 있는 특수 문자 제거
    text = re.sub('[=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', readData)
    return text.replace(' ', '')


def modify_item_name(item_row_name: str):
    try:
        idex_list = [(a.start(), a.end()) for a in list(re.finditer(' - ', item_row_name))]
        if len(idex_list) > 1:
            item_name = item_row_name[:idex_list[1][0]]
        else:
            item_name = item_row_name[:idex_list[0][0]]
    except:
        return item_row_name
    else:
        return item_name


def check_items_without_option(soup, writer, item):
    item_stock_status = item[2]

    # print(check_sold_out(soup))
    # print(check_temporary_sould_out(soup, item))

    if check_sold_out(soup) or check_temporary_sould_out(soup, item):
        # 갤러리아몰 품절
        # print('품절')
        if item_stock_status == '판매중':
            item.append('있음->품절')
            writer.writerow(item)
    else:
        # 갤러리아몰 재고 있음
        # print('판매')
        if item_stock_status == '품절':
            item.append('품절->있음')
            writer.writerow(item)


def check_sold_out(soup: BeautifulSoup):
    deleted_item = soup.find(attrs={'class': 'lstNone'})
    if deleted_item:
        return True  # 완전 품절
    else:
        return False  # 완전 품절 아님


def check_temporary_sould_out(soup: BeautifulSoup, input_item):
    # 일시품절 여부를 검사한다

    input_item_name = cleanText(input_item[1].replace(' ', '')) # 비교를 위해서 특수 문제 제거
    input_item_price = int(input_item[3])
    is_sold_out = True

    try:
        item_list = soup.find(attrs={'id': 'crossList'}).find(attrs={'class': 'goods_list'}).find('ul').find_all('li')
        for item in item_list:
            item = item.find('dl')
            price = int(item.find(attrs={'class': 'prm'}).get_text().replace('정상가', '').replace(',', ''))
            brand = soup.find('em', attrs={'class': 'brd'}).get_text().replace(' ', '')
            name = cleanText(item.find(attrs={'class': 'tit'}).get_text()) # 비교를 위해서 특수 문자 제거

            # 상품이름에 브랜드가 없는 경우 추가해준다
            if brand not in name:
                name = brand + name

            # print(price)
            # print(name)

            # 상품이 여러개 있을수 있기때문에 이름과 가격이 같은 상품만 대상으로 한다
            if (input_item_name in name or name in input_item_name) and input_item_price == price:
                is_sold_out = item.find(attrs={'class': 'soldOut'})
                if is_sold_out:
                    is_sold_out = True
                else:
                    is_sold_out = False
                    return is_sold_out

    except:
        is_sold_out = False  # 임시 품절은 아님

    return is_sold_out


def run_process():
    item_list = [
        ['5393968967', '크리니크 iD 로션', '판매중', '55000', 'N']
    ]

    count = 0
    # item_list = get_item_list()
    writer = make_csv_writer()

    for item in item_list:

        response = requests.get(get_item_url(item[1]))
        soup = BeautifulSoup(response.text, 'lxml')
        check_items_without_option(
            soup=soup,
            writer=writer,
            item=item
        )

        count += 1
        if count % 10 == 0:
            print(count)


run_process()


