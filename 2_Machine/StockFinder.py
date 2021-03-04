import csv
import re
import urllib


# 검색 조건
# 1> 상품 검색은 스마트스토어 상품 명에서 옵션을 제외한 상품명으로 검색한다
# 2> 상품명 비교는 브랜드를 제외하고 비교한다

class NoOptionItemStockChecker:

    def __init__(self, stock_writer, price_writer):
        self.stock_writer = stock_writer
        self.price_writer = price_writer


    def get_item_url(self, item):
        encoded_item = urllib.parse.quote(item)
        url = f'https://www.galleria.co.kr/search/totalSearch.action?searchTerm={encoded_item}&page_idx=&cateLM=&totalFilter=&disp_type_cd_dq=10&mall_no=0000014&cateYn=&searchType=&searchNumCheck=&selectChkYn='
        return url


    def clean_text(self, readData):
        # 텍스트에 포함되어 있는 특수 문자 제거
        text = re.sub('[=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', readData)
        return text.replace(' ', '')


    def check_items_without_option(self, browser, item):
        # 아이템 리스트 내부 한개의 형식
        # [상품번호, 상품명, 판매상테 ,백화점정가]
        browser.get(url=self.get_item_url(item[1]))
        item_stock_status = item[2]

        # print(self.check_sold_out(browser))
        # print(self.check_temporary_sould_out(browser, item))

        if self.check_sold_out(browser) or self.check_temporary_sould_out(browser, item):
            # 갤러리아몰 품절
            # print('품절')
            if item_stock_status == '판매중':
                item.append('있음 -> 품절')
                self.stock_writer.writerow(item)
                # print(f'{item}')

            return False
        else:
            # 갤러리아몰 재고 있음
            # print('있음')
            if item_stock_status == '품절':
                item.append('품절 -> 있음')
                self.stock_writer.writerow(item)
                # print(f'{item}')

            return True


    def check_sold_out(self, browser):
        try:
            browser.find_element_by_class_name('lstNone')
        except:
            return False  # 완전 품절은 아님

        else:
            return True  # 완전 품절


    def check_temporary_sould_out(self, browser, input_item):
        input_item_name = self.clean_text(input_item[1])
        input_item_price = int(input_item[3])
        is_sold_out = True

        try:
            item_list = browser.find_element_by_id('crossList').find_element_by_class_name(
                'goods_list').find_element_by_tag_name('ul').find_elements_by_tag_name('li')

            for item in item_list:
                item = item.find_element_by_tag_name('dl')
                price = int(item.find_element_by_class_name('prm').text.replace(',', ''))
                brand = browser.find_element_by_class_name('brd').text.replace(' ', '')
                name = self.clean_text(item.find_element_by_class_name('tit').text)  # 비교를 위해서 특수 문자 제거

                # 브랜드 명을 제외하고 상품명을 비교한다 (검색은 브래드를 포함하여 했음)
                if brand in name:
                    name = name.replace(brand, '')
                if brand in input_item_name:
                    input_item_name = input_item_name.replace(brand, '')

                # 상품이 여러개 있을수 있기때문에 이름과 가격이 같은 상품만 대상으로 한다
                if (input_item_name in name or name in input_item_name):
                    # print('묘')
                    try:
                        item.find_element_by_class_name('soldOut')
                    except:
                        is_sold_out = False
                    else:
                        if input_item_price != price:
                            input_item.append(f'{input_item_price} -> {price}')
                            self.price_writer.writerow(input_item)

                        is_sold_out = True
                        return is_sold_out

        except:
            is_sold_out = False  # 임시 품절은 아님

        return is_sold_out


    def get_mall_goods_no(self, browser, input_item):
        input_item_name = self.clean_text(input_item[1])

        item_list = browser.find_element_by_id('crossList').find_element_by_class_name(
            'goods_list').find_element_by_tag_name('ul').find_elements_by_tag_name('li')

        for item in item_list:
            item = item.find_element_by_tag_name('dl')
            brand = browser.find_element_by_class_name('brd').text.replace(' ', '')
            name = self.clean_text(item.find_element_by_class_name('tit').text)  # 비교를 위해서 특수 문자 제거

            pre_goods_no = item.find_element_by_class_name('tit').find_element_by_tag_name('a').get_attribute(
                'onClick')
            goods_no = pre_goods_no.split(':')[1].split(',')[0].replace('\'', '').replace(' ', '')

            if brand in name:
                name = name.replace(brand, '')
            if brand in input_item_name:
                input_item_name = input_item_name.replace(brand, '')

            if (input_item_name in name or name in input_item_name):
                return goods_no

        return False

    def check_item_stock(self, browser, item):
        return self.check_items_without_option(
            browser=browser,
            item=item
        )
