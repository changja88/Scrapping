abc1 = '[12]우왕'
abc2 = '우왕'


def modify_mall_item_name(item_name: str):
    if item_name.startswith('['):
        end_index = item_name.index('[') + 1
        return item_name[end_index:1]
    else:
        return item_name

print(modify_mall_item_name(abc1))
print(modify_mall_item_name(abc2))
