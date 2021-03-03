import csv
import re


class ItemCollecter:


    def modify_item_name(self, item_row_name: str):
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


    def get_item_lists(self, ):
        # 아이템 리스트 내부 한개의 형식
        # [상품번호, 상품명, 판매상테 ,백화점정가]
        # row[17] -> 옵션유무

        item_list_with_option = []
        item_list_without_option = []

        with open('../1_Row/2021_03_03.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader)
            for row in reader:
                if row[17] == 'Y':
                    item_list_with_option.append([row[0], self.modify_item_name(row[4]), row[7], row[10]])
                else:
                    item_list_without_option.append([row[0], self.modify_item_name(row[4]), row[7], row[10]])

        return item_list_with_option, item_list_without_option
