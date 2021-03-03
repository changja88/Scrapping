import csv
from datetime import date

import ItemCollecter
import OptionFinder
from selenium import webdriver
import NoOptionItemStockChecker


def make_chrome_browser():
    # options = Options()
    # user_agent = UserAgent()
    # options.add_argument(f'user-agent={user_agent}')

    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument(
        'User-Agent= Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36'
    )

    browser = webdriver.Chrome('../chromedriver', options=options)
    return browser


def make_csv_writer_for_item_price():
    filename = f'../3_Result/{date.today()} 가격 변경해야하는 상품.csv'
    f = open(filename, 'w', encoding='utf-8-sig', newline='')
    writer = csv.writer(f)
    return writer


def make_csv_writer_for_no_option_item():
    filename = f'../3_Result/{date.today()} 옵션 없는 상품.csv'
    f = open(filename, 'w', encoding='utf-8-sig', newline='')
    writer = csv.writer(f)
    return writer


def make_csv_writer_for_option_item():
    filename = f'../3_Result/{date.today()} 옵션 있는 상품.csv'
    f = open(filename, 'w', encoding='utf-8-sig', newline='')
    writer = csv.writer(f)
    return writer


def run():
    '''
    옵션이 있는 상품과 없는 상품을 구분하여 조회한다
    1> 옵션이 없는 상품은 재고 여부만 조회한다
    2> 1번을 수행할때는 재고 여부와 가격 변동 여부를 같이 조회한다
    3> 옵션이 있는 상품은 갤러리아몰에 재고가 없는 경우 조회 하지 않는다
    :return:
    '''

    browser = make_chrome_browser()

    item_collecter = ItemCollecter.ItemCollecter()

    no_option_item_stocker_checker = NoOptionItemStockChecker.NoOptionItemStockChecker(
        stock_writer=make_csv_writer_for_option_item(),
        price_writer=make_csv_writer_for_item_price()
    )
    option_finder = OptionFinder.OptionFinder(
        browser=browser,
        writer=make_csv_writer_for_no_option_item()
    )

    item_list_with_option, item_list_without_option = item_collecter.get_item_lists()

    # [상품번호, 상품명, 판매상테, 백화점정가]
    item_list_with_option = [
        # TODO : 이거 재고 있음으로 나오게 해야함
        ['5116963713', '랑콤 어드밴스드 제니피끄 아이 크림 15ml', '판매중', '99000'],
        # ['5089479641', '디올 루즈 디올 울트라 루즈', '판매중', '48000']
    ]

    count = 0
    # for item in item_list_without_option:
    #     no_option_item_stocker_checker.check_item_stock(
    #         browser=browser,
    #         item=item,
    #     )
    #     count += 1
    #     if count % 10 == 0:
    #         print(count)

    count = 0
    for item in item_list_with_option:
        is_in_stock = no_option_item_stocker_checker.check_item_stock(
            browser=browser,
            item=item,
        )
        # 갤러리아 몰에 재고가 있는 경우에는 옵션 품절 확인한다
        if is_in_stock:
            goods_no = no_option_item_stocker_checker.get_mall_goods_no(
                browser=browser,
                input_item=item
            )
            if goods_no:
                option_finder.compare_option(
                    item=item,
                    goods_no=goods_no
                )
        count += 1
        if count % 10 == 0:
            print(count)


run()
