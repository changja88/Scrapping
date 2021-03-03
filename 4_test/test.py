first = {
    'valid': [1, 3, ],
    'soldout': [6, 7]
}

second = {
    'valid': [1, ],
    'soldout': [6,]
}

need_to_be_sold_out = []
for valid in first['valid']:

    # 품절 시켜야할 옵션
    if valid not in second['valid']:
        need_to_be_sold_out.append(valid)



need_to_be_add = []
for soldout in first['soldout']:

    if soldout in second['valid']:
        need_to_be_add.append(soldout)


