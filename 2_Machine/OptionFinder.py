class SmartStoreItemOptionFinder:

    def make_url(self, item_number):
        return f'https://smartstore.naver.com/in_bloomington/products/{item_number}'

    def get_item_option_list(self, browser, item_id):
        invalid_option_list = ['제품 브랜드 쇼핑백 (+1,000원)', '선물포장재(+1,000원)']

        result_option_list = {}
        valid_options = []
        soldout_options = []

        browser.get(self.make_url(item_id))
        option_btn = browser.find_element_by_class_name('_3NaJVRY_EO')
        option_btn.click()

        # 선물 포장 옵션만 있는 경우에는 넘어가기 위해서 try처리
        try:
            option_list = browser.find_element_by_class_name('_1VTfy4KOtG').find_elements_by_tag_name('li')
            for option in option_list:
                option = option.text.replace(' ', '')
                if option not in invalid_option_list:
                    if '(품절)' in option:
                        result = option.replace('(품절)', '')
                        soldout_options.append(result)
                    else:
                        valid_options.append(option)
        except:
            pass

        result_option_list['valid'] = valid_options
        result_option_list['soldout'] = soldout_options

        return result_option_list


class MallItemOptionFinder:

    def make_url(self, goods_no):
        return f'https://www.galleria.co.kr/goods/initDetailGoods.action?target=_self&goods_no={goods_no}'


    def get_item_option_list(self, browser, goods_no):
        invalid_option_list = ['옵션검색하기']

        valid_options = []
        soldout_options = []
        result_option_list = {}

        browser.get(self.make_url(goods_no))

        try:
            # 묶음 상품의 경우 갤러리아몰에 옵션으로 존재 하지 않아서 try로 처리
            option_btn = browser.find_element_by_id('opt_btn_top_1')
            option_btn.click()

            option_list = browser.find_element_by_name('option_list').find_elements_by_tag_name('li')

            for option in option_list:
                option = option.text.replace(' ', '')
                if option not in invalid_option_list:
                    if '(품절)' in option:
                        result = option.replace('(품절)', '')
                        soldout_options.append(result)
                    else:
                        valid_options.append(option)

            result_option_list['valid'] = valid_options
            result_option_list['soldout'] = soldout_options
            return result_option_list

        except:
            result_option_list['valid'] = valid_options
            result_option_list['soldout'] = soldout_options
            return result_option_list


class OptionFinder:

    def __init__(self, browser, writer):
        self.smart_store_option_finder = SmartStoreItemOptionFinder()
        self.mall_option_finder = MallItemOptionFinder()
        self.browser = browser
        self.writer = writer

    def compare_option(self, item, goods_no):
        store_options = self.smart_store_option_finder.get_item_option_list(
            browser=self.browser,
            item_id=item[0]
        )
        mall_options = self.mall_option_finder.get_item_option_list(
            browser=self.browser,
            goods_no=goods_no
        )

        need_to_be_sold_out = []
        for valid in store_options['valid']:
            # 품절 시켜야할 옵션
            if valid not in mall_options['valid']:
                need_to_be_sold_out.append(valid)

        need_to_be_add = []
        for valid in mall_options['valid']:
            if valid not in store_options['valid']:
                need_to_be_add.append(valid)

        if len(need_to_be_sold_out) > 1 or len(need_to_be_add):
            self.writer.writerow([item[0], item[1]])

            if len(need_to_be_sold_out) > 1:
                self.writer.writerow(['품절 처리해야할 옵션'])
                self.writer.writerow(need_to_be_sold_out)
            if len(need_to_be_add) > 1:
                self.writer.writerow(['추가해야할  옵션'])
                self.writer.writerow(need_to_be_add)

        return need_to_be_sold_out, need_to_be_add
