# 분실 / 습득 지역명을 지역코드로 변환하는 메소드 (도, 광역시 단위만 가능)
def location_to_code(location_name):
    if '서울' in location_name:
        location_code = 'LCA000'
    elif '강원' in location_name:
        location_code = 'LCH000'
    elif '경기' in location_name:
        location_code = 'LCI000'
    elif '경상남도' in location_name or '경남' in location_name:
        location_code = 'LCJ000'
    elif '경상북도' in location_name or '경북' in location_name:
        location_code = 'LCK000'
    elif '광주' in location_name:
        location_code = 'LCQ000'
    elif '대구' in location_name:
        location_code = 'LCR000'
    elif '대전' in location_name:
        location_code = 'LCS000'
    elif '부산' in location_name:
        location_code = 'LCT000'
    elif '울산' in location_name:
        location_code = 'LCU000'
    elif '인천' in location_name:
        location_code = 'LCV000'
    elif '전라남도' in location_name or '전남' in location_name:
        location_code = 'LCL000'
    elif '전라북도' in location_name or '전북' in location_name:
        location_code = 'LCM000'
    elif '충청남도' in location_name or '충남' in location_name:
        location_code = 'LCN000'
    elif '충청북도' in location_name or '충북' in location_name:
        location_code = 'LCO000'
    elif '제주' in location_name:
        location_code = 'LCP000'
    elif '세종' in location_name:
        location_code = 'LCW000'
    elif '해외' in location_name:
        location_code = 'LCF000'
    else:
        location_code = 'LCE000'

    return location_code


# 유실물 분류명을 분류코드로 변환하는 메소드
def category_to_code(main_category_name, sub_category_name):
    sub_category_code = None

    if main_category_name == '가방':
        main_category_code = 'PRA000'

        if sub_category_name is not None:
            if '여성' in sub_category_name:
                sub_category_code = 'PRA100'
            elif '남성' in sub_category_name:
                sub_category_code = 'PRA200'
            else:
                sub_category_code = 'PRA300'
    elif main_category_name == '귀금속':
        main_category_code = 'PRO000'

        if sub_category_name is not None:
            if sub_category_name == '반지':
                sub_category_code = 'PRO100'
            elif sub_category_name == '목걸이':
                sub_category_code = 'PRO200'
            elif sub_category_name == '귀걸이':
                sub_category_code = 'PRO300'
            elif sub_category_name == '시계':
                sub_category_code = 'PRO400'
            else:
                sub_category_code = 'PRO500'
    elif main_category_name == '도서용품':
        main_category_code = 'PRB000'

        if sub_category_name is not None:
            if sub_category_name == '학습서적':
                sub_category_code = 'PRB100'
            elif sub_category_name == '소설':
                sub_category_code = 'PRB200'
            elif sub_category_name == '컴퓨터서적':
                sub_category_code = 'PRB300'
            elif sub_category_name == '만화책':
                sub_category_code = 'PRB400'
            else:
                sub_category_code = 'PRB500'
    elif main_category_name == '서류':
        main_category_code = 'PRC000'

        if sub_category_name is not None:
            if sub_category_name == '서류':
                sub_category_code = 'PRC100'
            else:
                sub_category_code = 'PRC200'
    elif main_category_name == '산업용품':
        main_category_code = 'PRD000'
        sub_category_code = 'PRD100'
    elif main_category_name == '쇼핑백':
        main_category_code = 'PRQ000'
        sub_category_code = 'PRQ100'
    elif main_category_name == '스포츠용품':
        main_category_code = 'PRE000'
        sub_category_code = 'PRE100'
    elif main_category_name == '악기':
        main_category_code = 'PRR000'

        if sub_category_name is not None:
            if sub_category_name == '건반악기':
                sub_category_code = 'PRR100'
            elif sub_category_name == '관악기':
                sub_category_code = 'PRR200'
            elif sub_category_name == '타악기':
                sub_category_code = 'PRR300'
            elif sub_category_name == '현악기':
                sub_category_code = 'PRR400'
            else:
                sub_category_code = 'PRR900'
    elif main_category_name == '유가증권':
        main_category_code = 'PRM000'

        if sub_category_name is not None:
            if sub_category_name == '어음':
                sub_category_code = 'PRM100'
            elif sub_category_name == '상품권':
                sub_category_code = 'PRM200'
            elif sub_category_name == '채권':
                sub_category_code = 'PRM300'
            else:
                sub_category_code = 'PRM400'
    elif main_category_name == '의류':
        main_category_code = 'PRK000'

        if sub_category_name is not None:
            if '여성' in sub_category_name:
                sub_category_code = 'PRK100'
            elif '남성' in sub_category_name:
                sub_category_code = 'PRK200'
            elif '아기' in sub_category_name:
                sub_category_code = 'PRK300'
            else:
                sub_category_code = 'PRK400'
    elif main_category_name == '자동차':
        main_category_code = 'PRF000'

        if sub_category_name is not None:
            if sub_category_name == '자동차열쇠':
                sub_category_code = 'PRF100'
            elif sub_category_name == '네비게이션' or sub_category_name == '내비게이션':
                sub_category_code = 'PRF200'
            elif sub_category_name == '자동차번호판':
                sub_category_code = 'PRF300'
            elif sub_category_name == '임시번호판':
                sub_category_code = 'PRF500'
            else:
                sub_category_code = 'PRF400'
    elif main_category_name == '전자기기':
        main_category_code = 'PRG000'

        if sub_category_name is not None:
            if sub_category_name == 'PMP':
                sub_category_code = 'PRG100'
            elif sub_category_name == 'MP3':
                sub_category_code = 'PRG200'
            elif sub_category_name == 'PDA':
                sub_category_code = 'PRG300'
            elif sub_category_name == '카메라':
                sub_category_code = 'PRG400'
            elif sub_category_name == '전자수첩':
                sub_category_code = 'PRG500'
            else:
                sub_category_code = 'PRG600'
    elif main_category_name == '지갑':
        main_category_code = 'PRH000'

        if sub_category_name is not None:
            if '여성' in sub_category_name:
                sub_category_code = 'PRH100'
            elif '남성' in sub_category_name:
                sub_category_code = 'PRH200'
            else:
                sub_category_code = 'PRH300'
    elif main_category_name == '증명서':
        main_category_code = 'PRN000'

        if sub_category_name is not None:
            if sub_category_name == '신분증':
                sub_category_code = 'PRN100'
            elif sub_category_name == '면허증':
                sub_category_code = 'PRN200'
            elif sub_category_name == '여권':
                sub_category_code = 'PRN300'
            else:
                sub_category_code = 'PRN400'
    elif main_category_name == '컴퓨터':
        main_category_code = 'PRI000'

        if sub_category_name is not None:
            if '삼성' in sub_category_name:
                sub_category_code = 'PRI100'
            elif 'LG' in sub_category_name:
                sub_category_code = 'PRI200'
            elif '삼보' in sub_category_name:
                sub_category_code = 'PRI300'
            elif 'HP' in sub_category_name:
                sub_category_code = 'PRI500'
            else:
                sub_category_code = 'PRI400'
    elif main_category_name == '카드':
        main_category_code = 'PRP000'

        if sub_category_name is not None:
            if '신용' in sub_category_name or '체크' in sub_category_name:
                sub_category_code = 'PRP100'
            elif sub_category_name == '일반카드':
                sub_category_code = 'PRP200'
            else:
                sub_category_code = 'PRP300'
    elif main_category_name == '현금':
        main_category_code = 'PRL000'

        if sub_category_name is not None:
            if sub_category_name == '현금':
                sub_category_code = 'PRL100'
            elif sub_category_name == '수표':
                sub_category_code = 'PRL200'
            elif sub_category_name == '외화':
                sub_category_code = 'PRL400'
            else:
                sub_category_code = 'PRL300'
    elif main_category_name == '휴대폰':
        main_category_code = 'PRJ000'

        if sub_category_name is not None:
            if '모토로라' in sub_category_name:
                sub_category_code = 'PRJ600'
            elif '삼성' in sub_category_name:
                sub_category_code = 'PRJ100'
            elif 'LG' in sub_category_name:
                sub_category_code = 'PRJ200'
            elif '스카이' in sub_category_name:
                sub_category_code = 'PRJ300'
            elif '아이폰' in sub_category_name:
                sub_category_code = 'PRJ400'
            else:
                sub_category_code = 'PRJ500'
    else:
        main_category_code = 'PRZ000'
        sub_category_code = 'PRZ100'

    if sub_category_code is not None:
        return main_category_code, sub_category_code
    else:
        return main_category_code
