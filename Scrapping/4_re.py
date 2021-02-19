# 정규식

import re

if __name__ == '__main__':

    p = re.compile('ca.e')
    # . (ca.e) -> 하나의 문자를 의미 care, cafe, case
    # ^ (^de) -> 문자열의 시작 desk, destination , fade(x)
    # $ (se$) -> 문자열의 끝 case, base, face(X)

    m = p.match('case')
    # 주어진 문자열의 처음부터 일치하는지 확인
    # 따라서 careless 를 넣어줘도 매치한다
    if m :
        print(m.group())
    else:
        print('매칭 되지 않음')


    m = p.search('good care')
    # 주어진 문자열 중에 일치하는게 있는지 확인
    if m:
        print(m.group()) # -> 일치하는 문자열 반환
        print(m.string) # -> 입력받은 문자열 반환
        print(m.start()) # -> 일치하는 문자열의 시작 인덱스
        print(m.end()) # -> 일치하는 문자열의 끝 인덱스
        print(m.span()) # -> 일치하는 문자열의 시작, 끝 인덱스
    else:
        print('매칭 되지 않음')


    list = p.findall('careless')
    # 일치하는 모든 것을 리스트 형태로 반환
    print(list)


