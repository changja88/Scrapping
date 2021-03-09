import csv
from datetime import date
import time

import ItemCollecter
import OptionFinder
from selenium import webdriver
import StockFinder


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

    start_time = time.time()
    browser = make_chrome_browser()
    item_collecter = ItemCollecter.ItemCollecter()
    item_list_with_option, item_list_without_option = item_collecter.get_item_lists()

    no_option_item_stocker_checker = StockFinder.NoOptionItemStockChecker(
        stock_writer=make_csv_writer_for_no_option_item(),
        price_writer=make_csv_writer_for_item_price()
    )
    option_finder = OptionFinder.OptionFinder(
        browser=browser,
        writer=make_csv_writer_for_option_item()
    )

    # item_list_without_option = [
    #     ['5116963713', '랑콤 어드밴스드 제니피끄 아이 크림 15ml', '판매중', '1'],
    #     ['5089479641', '메이크업포에버 228 프리시젼 아이 섀이더 브러쉬 미디엄', '판매중', '1']
    # ]
    #
    # item_list_with_option = [
    #     ['5232394679','산타마리아노벨라 아쿠아 디 콜로니아 - 시타 디 교토','판매중','218000'],
    # ]


    count = 0
    for item in item_list_without_option:
        no_option_item_stocker_checker.check_item_stock(
            browser=browser,
            item=item,
        )
        count += 1
        if count % 10 == 0:
            print(count)

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
                result = option_finder.compare_option(
                    item=item,
                    goods_no=goods_no
                )
                print(result)

        count += 1
        if count % 10 == 0:
            print(count)

    browser.close()
    browser.quit()

    end_time = time.time()
    processing_time = end_time - start_time
    print(f'처리시간 {processing_time}')


run()
