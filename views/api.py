"""
유실물 통합 조회 API
한국기술교육대학교 서비스지향컴퓨팅및실습 텀 프로젝트 2조
2014136019 김성찬
2014136030 김쾌남

특징
1. 기존에 분리되어있는 오퍼레이션을 하나로 통합,
   하나의 API에 원하는 파라미터를 전달하는 것만으로 사용자가 원하는 오퍼레이션을 알아서 수행
2. 기존 API는 응답을 XML로만 제공하지만, 본 API는 JSON 형식으로 반환하므로
   공공데이터포털 OPEN API의 대체품으로 사용 가능
3. 특히 경찰청에 온/오프라인으로 신고한 분실물의 경우 경찰서뿐만 아니라
   포털기관(지하철, 백화점 등)에서 습득한 유실물 중 유사한 물품을 리스트로 제공,
   별도로 2개 이상의 API를 사용하여 조회할 필요가 없음
4. 분류별, 지역별, 기간별로 유실물을 조회할 경우 해당하는 코드를 알아야 API를 사용할 수 있는 단점 극복
5. 분실물 조회의 경우 파라미터에 예상 습득물 매칭 여부 옵션을 추가하여
   불필요한 쿼리를 방지함 -> 속도 증가

"""

from flask import Blueprint, json, request, make_response
from views.code_converter import location_to_code, category_to_code
import requests
import xmltodict
from keys import OPEN_API_SERVICE_KEY

# 블루프린트 등록
api_blueprint = Blueprint('api', __name__)

# 서비스 키
service_key = OPEN_API_SERVICE_KEY

# 요청 API 호스트 URL
host_url = 'http://apis.data.go.kr/1320000'

# API 엔드 포인트
lost_end_point = '/LostGoodsInfoInqireService'
found_end_point = '/LosfundInfoInqireService'
portal_end_point = '/LosPtfundInfoInqireService'
# mobile_end_point = '/SearchMoblphonInfoInqireService'

# API 요청 주소
lost_search_np_url = host_url + lost_end_point + '/getLostGoodsInfoAccTpNmCstdyPlace'
lost_search_cd_url = host_url + lost_end_point + '/getLostGoodsInfoAccToClAreaPd'
lost_detail_url = host_url + lost_end_point + '/getLostGoodsDetailInfo'
found_search_np_url = host_url + found_end_point + '/getLosfundInfoAccTpNmCstdyPlace'
found_search_cd_url = host_url + found_end_point + '/getLosfundInfoAccToClAreaPd'
found_detail_url = host_url + found_end_point + '/getLosfundDetailInfo'
portal_search_np_url = host_url + portal_end_point + '/getPtLosfundInfoAccTpNmCstdyPlace'
portal_search_cd_url = host_url + portal_end_point + '/getPtLosfundInfoAccToClAreaPd'
portal_detail_url = host_url + portal_end_point + '/getPtLosfundDetailInfo'
# mobile_search_url = host_url + mobile_end_point + '/getMoblphonAcctoKindAreaPeriodInfo'
# mobile_detail_url = host_url + mobile_end_point + '/getMoblphonDetailInfo'

# 분실물 / 습득물 목록 건수 디폴트값
LOST_NUM_OF_ROWS = 10
FOUND_NUM_OF_ROWS = 10


@api_blueprint.route('/lostInfo')
def lost_search():
    """ 기능 1.
        분실물을 물품명이나 분실 장소, 물품 종류나 신고 날짜로 검색 시
        예상되는 습득물의 상세 정보를 리스트로 출력
        (분실물의 분실 장소 혹은 색상과 일치하는 신고 날짜 이후의 습득물 리스트)
        (명칭, 장소별 / 분류, 기간별로 분리된 API를 하나로 통합)
    """
    # case 1. 명칭, 장소별 / 분류, 기간별 모두 빈 칸일 때
    #         -> 명칭, 장소별 url에 pageNo, numOfRows 파라미터만 전달하여 요청
    # case 2. 명칭, 장소별 파라미터만 채워져있을 때
    #         -> 명칭, 장소별로 조회
    # case 3. 분류, 기간별 파라미터만 채워져있을 때
    #         -> 분류, 기간별로 조회
    # case 4. 명칭, 장소별 / 분류, 기간별 모두 채워져있을 때
    #         -> 분류, 기간별 조회 API를 베이스로 pageNo를 증가시켜가면서
    #         -> LST_PRDT_NM이 lstPrdtNm 문자열 내에 있고 LST_PLACE가 lstPlace 문자열 내에 있는지 검사
    #         -> 만약 lostNumOfRows만큼 찾으면 루프 종료

    # API를 요청하는 데 사용할 파라미터 객체
    params = {}

    # 파라미터 입력 여부에 따라 객체에 저장
    if request.args.get('lostPlace') is not None:
        params['LST_PLACE'] = request.args.get('lostPlace')
    if request.args.get('brandName') is not None:
        params['LST_PRDT_NM'] = request.args.get('brandName')
    if request.args.get('startDate') is not None:
        params['START_YMD'] = request.args.get('startDate')
    if request.args.get('endDate') is not None:
        params['END_YMD'] = request.args.get('endDate')

    # 유실물 분류명을 코드로 변환 (상위분류, 혹은 상위 / 하위분류 파라미터가 모두 채워져 있을 경우에만)
    if request.args.get('mainCategory') is not None:
        if request.args.get('subCategory') is not None:
            params['PRDT_CL_CD_01'], params['PRDT_CL_CD_02'] = \
                category_to_code(request.args.get('mainCategory'), request.args.get('subCategory'))
        else:
            params['PRDT_CL_CD_01'] = category_to_code(request.args.get('mainCategory'), None)

    # 분실 지역명을 코드로 변환
    if request.args.get('lostPlaceSiDo') is not None:
        params['LST_LCT_CD'] = location_to_code(request.args.get('lostPlaceSiDo'))

    # 페이지 번호, 목록 건수 파라미터가 있으면 객체 저장, 없으면 디폴트값을 객체에 저장
    if request.args.get('pageNo') is not None:
        params['pageNo'] = request.args.get('pageNo')
    else:
        params['pageNo'] = 1
    if request.args.get('lostNumOfRows') is not None:
        params['numOfRows'] = request.args.get('lostNumOfRows')
    else:
        params['numOfRows'] = LOST_NUM_OF_ROWS

    # 예상 습득물 목록 출력 여부 파라미터가 있을 때 1이면 True, 0이면 False
    # 그 외의 값이나 파라미터 자체가 없을 땐 디폴트 값 True
    is_get_predicted_items = True
    if request.args.get('getPredictedItems') is not None:
        if request.args.get('getPredictedItems') == '0':
            is_get_predicted_items = False

    # 최종적으로 출력할 JSON
    result = {
        'items': [],
        'lostPageNo': params['pageNo'],
        'lostNumOfRows': params['numOfRows']
    }

    if is_get_predicted_items:
        # 습득물 목록 건수 파라미터가 있으면 객체 저장, 없으면 디폴트값을 객체에 저장
        if request.args.get('maxFoundNumOfRows') is not None:
            result['maxFoundNumOfRows'] = request.args.get('maxFoundNumOfRows')
        else:
            result['maxFoundNumOfRows'] = FOUND_NUM_OF_ROWS

    # 분실물 리스트
    lost_goods_list = []

    if 'START_YMD' not in params.keys() and 'END_YMD' not in params.keys() and 'PRDT_CL_CD_01' not in params.keys() \
            and 'PRDT_CL_CD_02' not in params.keys() and 'LST_LCT_CD' not in params.keys():
        # 분류, 기간별 조회 API 파라미터가 모두 빈 칸일 때
        # -> 파라미터 존재 여부에 상관 없이 명칭, 장소별 조회 API를 사용

        lost_goods_list = get_response_and_convert(lost_search_np_url, params)
    else:
        # 분류, 기간별 조회 API 파라미터가 하나라도 채워져있을 때
        # -> 파라미터 존재 여부에 상관 없이 분류, 기간별 조회 API를 사용
        # -> 단, 명칭, 장소별 조회 API 파라미터가 하나라도 있으면 분실물명 및 장소명이 결과와 일치하는지 하나씩 검사

        if 'LST_PLACE' not in params.keys() and 'LST_PRDT_NM' not in params.keys():
            # 명칭, 장소별 조회 API 파라미터가 모두 빈 칸일 때

            lost_goods_list = get_response_and_convert(lost_search_cd_url, params)
        else:
            # 명칭, 장소별 조회 API 파라미터가 하나라도 채워져있을 때
            # 단, 여기서 numOfRows는 1000으로 고정한다. (디폴트값인 10으로 유지하면 속도 감소)

            page_no = 1
            max_candidate_num = int(params['numOfRows'])
            params['numOfRows'] = 1000
            while True:
                params['pageNo'] = page_no
                candidates = get_response_and_convert(lost_search_cd_url, params)
                if candidates is None:
                    break

                for candidate in candidates:
                    # 파라미터 존재 여부에 따라 분실물의 해당 파라미터와 일치하는지 검사
                    if 'LST_PLACE' in params.keys() and 'LST_PRDT_NM' in params.keys():
                        if params['LST_PLACE'] in candidate['lstPlace'] \
                                and params['LST_PRDT_NM'] in candidate['lstPrdtNm']:
                            lost_goods_list.append(candidate)
                            max_candidate_num -= 1
                    elif 'LST_PLACE' in params.keys():
                        if params['LST_PLACE'] in candidate['lstPlace']:
                            lost_goods_list.append(candidate)
                            max_candidate_num -= 1
                    elif 'LST_PRDT_NM' in params.keys():
                        if params['LST_PRDT_NM'] in candidate['lstPrdtNm']:
                            lost_goods_list.append(candidate)
                            max_candidate_num -= 1

                    if max_candidate_num == 0:
                        break

                # 분실물 목록 건수 만큼 선택이 완료되면 루프 종료
                if max_candidate_num == 0:
                    break
                else:
                    page_no += 1

    # 분실물 리스트 아이템의 개수
    # (lostNumOfRows보다 작을 경우 lostNumOfRows 대신 들어갈 값)
    num_of_item = 0

    # 각 분실물의 상세정보를 리스트에 저장
    for item in lost_goods_list:
        params_id = {
            'ATC_ID': item['atcId']
        }

        # 분실물 리스트의 상세정보를 요청
        details_result = get_response_and_convert(lost_detail_url, params_id)

        # 물품분류명을 상위분류명과 하위분류명으로 분리
        product_category = details_result['prdtClNm'].split(' > ')

        # 분실물 상세정보 리스트 아이템 객체
        lost_goods_result = {
            'id': details_result['atcId'],
            'image': details_result['lstFilePathImg'],
            'lostHour': details_result['lstHor'],
            'lostLocationName': details_result['lstLctNm'],
            'lostPlace': details_result['lstPlace'],
            'lostPlaceSub': details_result['lstPlaceSeNm'],
            'lostProductName': details_result['lstPrdtNm'],
            'lostSubject': details_result['lstSbjt'],
            'lostStateName': details_result['lstSteNm'],
            'lostYMD': details_result['lstYmd'],
            'orgName': details_result['orgNm'],
            'orgId': details_result['orgId'],
            'productCategory': product_category[0],
            'productCategorySub': product_category[1],
            'tel': details_result['tel'],
        }
        # 응답 결과에 색상코드가 있다면 리스트 아이템 객체에 색상코드 추가
        if 'clrNm' in details_result.keys():
            lost_goods_result['color'] = details_result['clrNm']

        # 예상 습득물 리스트 표시 여부가 True일 경우
        if is_get_predicted_items:
            # 1. 찾은 날짜 > 잃어버린 날짜 (날짜가 같을 경우 발견한 시간 > 잃어버린 시간)
            # 2. 보관 중인 장소 = 신고한 장소, else 잃어버린 장소 근처 포털기관 위치
            # 참고: 찾은 물품 = 잃어버린 물품 -> 검색이 잘 안됨
            # 정규표현식으로 어절 단위 분리, 각 어절이 포함된 물품 검사 -> 가능하지만 검색 속도 증가
            # 따라서 마지막 어절만 추출, 검색에 활용

            # 예상 습득물 리스트를 객체에 추가
            lost_goods_result['predictedItems'] = []

            # 습득물(경찰서, 포털기관) 조회를 위한 파라미터 객체
            params_found = {
                'PRDT_NM': lost_goods_result['lostProductName'].split(' ')[-1],
                'DEP_PLACE': lost_goods_result['orgName'],
                'numOfRows': 1000
            }

            # 경찰서, 포털기관 습득물 조회 결과(candidate)에서 가져올 아이템 개수
            max_candidate_num = int(result['maxFoundNumOfRows'])

            # 경찰서 습득물 조회
            # print('다음으로 검색:', params_found['PRDT_NM'])
            page_no = 1
            while True:
                # 분실물 목록 건수 만큼 선택이 완료되면 루프 종료
                if max_candidate_num == 0:
                    break

                params_found['pageNo'] = page_no
                candidates = get_response_and_convert(found_search_np_url, params_found)
                if candidates is None:
                    break

                for candidate in candidates:
                    if 'fdYmd' not in candidate.keys():
                        matched_goods = get_found_item(candidate, found_detail_url)
                        if matched_goods is None:
                            matched_goods = get_found_item(candidate, None)

                        lost_goods_result['predictedItems'].append(matched_goods)
                        max_candidate_num -= 1
                    else:
                        if int(candidate['fdYmd'].replace('-', '')) > int(lost_goods_result['lostYMD'].replace('-', '')):
                            # 습득물을 찾은 날이 분실물을 잃어버린 날보다 나중일 경우에만 리스트에 추가
                            matched_goods = get_found_item(candidate, found_detail_url)
                            if matched_goods is None:
                                matched_goods = get_found_item(candidate, None)

                            lost_goods_result['predictedItems'].append(matched_goods)
                            max_candidate_num -= 1
                        elif int(candidate['fdYmd'].replace('-', '')) == int(lost_goods_result['lostYMD'].replace('-', '')):
                            # 만약 찾은 날과 잃어버린 날이 같을 경우 습득물을 찾은 시간이 잃어버린 날보다 나중일 경우에만 추가
                            if 'fdHor' in candidate.keys():
                                if int(candidate['fdHor']) >= int(lost_goods_result['lostHour']):
                                    matched_goods = get_found_item(candidate, found_detail_url)
                                    if matched_goods is None:
                                        matched_goods = get_found_item(candidate, None)

                                    lost_goods_result['predictedItems'].append(matched_goods)
                                    max_candidate_num -= 1

                    if max_candidate_num == 0:
                        break

                page_no += 1

            # 포털기관 습득물 조회
            params_found['DEP_PLACE'] = ''
            page_no = 1
            while True:
                # 분실물 목록 건수 만큼 선택이 완료되면 루프 종료
                if max_candidate_num == 0:
                    break

                params_found['pageNo'] = page_no
                candidates = get_response_and_convert(portal_search_np_url, params_found)
                if candidates is None:
                    break

                for candidate in candidates:
                    if 'fdYmd' not in candidate.keys():
                        matched_goods = get_found_item(candidate, portal_detail_url)
                        if matched_goods is None:
                            matched_goods = get_found_item(candidate, None)

                        lost_goods_result['predictedItems'].append(matched_goods)
                        max_candidate_num -= 1
                    else:
                        if int(candidate['fdYmd'].replace('-', '')) > int(lost_goods_result['lostYMD'].replace('-', '')):
                            # 습득물을 찾은 날이 분실물을 잃어버린 날보다 나중일 경우에만 리스트에 추가
                            matched_goods = get_found_item(candidate, portal_detail_url)
                            if matched_goods is None:
                                matched_goods = get_found_item(candidate, None)

                            lost_goods_result['predictedItems'].append(matched_goods)
                            max_candidate_num -= 1
                        elif int(candidate['fdYmd'].replace('-', '')) == int(lost_goods_result['lostYMD'].replace('-', '')):
                            # 만약 찾은 날과 잃어버린 날이 같을 경우 습득물을 찾은 시간이 잃어버린 날보다 나중일 경우에만 추가
                            if 'fdHor' in candidate.keys():
                                if int(candidate['fdHor']) >= int(lost_goods_result['lostHour']):
                                    matched_goods = get_found_item(candidate, portal_detail_url)
                                    if matched_goods is None:
                                        matched_goods = get_found_item(candidate, None)

                                    lost_goods_result['predictedItems'].append(matched_goods)
                                    max_candidate_num -= 1

                    if max_candidate_num == 0:
                        break

                page_no += 1

        result['items'].append(lost_goods_result)
        num_of_item += 1

    # 리스트 아이템 개수가 lostNumOfRows보다 작다면 lostNumOfRows 갱신
    if num_of_item < int(result['lostNumOfRows']):
        result['lostNumOfRows'] = num_of_item

    # jsonify()로 리턴하면 한글이 유니코드 문자열로 변환되어서 출력됨
    # https://soooprmx.com/archives/6788
    # return jsonify(result)
    # return json.dumps(result, ensure_ascii=False)
    response = make_response(json.dumps(result, ensure_ascii=False))
    response.headers['Content-Type'] = 'application/json;charset=UTF-8'
    response.headers['mimetype'] = 'application/json'
    return response


@api_blueprint.route('/foundInfo')
def found_search():
    """ 기능 2.
        습득물을 물품명이나 습득 장소로 검색 시
        경찰서 뿐만 아니라 포털기관(지하철, 쇼핑몰 등)에서
        습득한 물품을 통합해서 상세 정보를 리스트로 출력
        (기존 API와는 다르게 습득물 및 포털기관 검색 결과를 통합하여 제공)
    """
    # 명칭, 장소별 / 분류, 기간별 조회는 기능 1과 동일
    # 단, 경찰서(지구대) 습득물과 포털기관(지하철, 백화점 등) 습득물을 모두 출력해야 함

    # API를 요청하는 데 사용할 파라미터 객체
    params = {}

    # 파라미터 입력 여부에 따라 객체에 저장
    if request.args.get('foundPlace') is not None:
        params['DEP_PLACE'] = request.args.get('foundPlace')
    if request.args.get('foundName') is not None:
        params['PRDT_NM'] = request.args.get('foundName')
    if request.args.get('startDate') is not None:
        params['START_YMD'] = request.args.get('startDate')
    if request.args.get('endDate') is not None:
        params['END_YMD'] = request.args.get('endDate')

    # 유실물 분류명을 코드로 변환 (상위분류, 혹은 상위 / 하위분류 파라미터가 모두 채워져 있을 경우에만)
    if request.args.get('mainCategory') is not None:
        if request.args.get('subCategory') is not None:
            params['PRDT_CL_CD_01'], params['PRDT_CL_CD_02'] = \
                category_to_code(request.args.get('mainCategory'), request.args.get('subCategory'))
        else:
            params['PRDT_CL_CD_01'] = category_to_code(request.args.get('mainCategory'), None)

    # 습득 지역명을 코드로 변환
    if request.args.get('foundPlaceCode') is not None:
        params['N_FD_LCT_CD'] = location_to_code(request.args.get('foundPlaceCode'))

    # 색상코드 (경찰서, 포털기관) (미사용)
    # if request.args.get('colorCode') is not None:
    #     params['CLR_CD'] = request.args.get('colorCode')
    #     params['FD_COL_CD'] = request.args.get('colorCode')

    # 페이지 번호, 목록 건수 파라미터가 있으면 객체 저장, 없으면 디폴트값을 객체에 저장
    if request.args.get('pageNo') is not None:
        params['pageNo'] = request.args.get('pageNo')
    else:
        params['pageNo'] = 1
    if request.args.get('foundNumOfRows') is not None:
        params['numOfRows'] = request.args.get('foundNumOfRows')
    else:
        params['numOfRows'] = FOUND_NUM_OF_ROWS

    # 최종적으로 출력할 JSON
    result = {
        'foundItems': [],
        'portalItems': [],
        'foundPageNo': params['pageNo'],
        'foundNumOfRows': params['numOfRows'],
        'portalPageNo': params['pageNo'],
        'portalNumOfRows': params['numOfRows']
    }

    # 습득물 리스트 (경찰서, 포털기관)
    found_goods_list = []
    portal_goods_list = []

    if 'START_YMD' not in params.keys() and 'END_YMD' not in params.keys() \
            and 'PRDT_CL_CD_01' not in params.keys() and 'PRDT_CL_CD_02' not in params.keys() \
            and 'N_FD_LCT_CD' not in params.keys() and 'FD_COL_CD' not in params.keys() \
            and 'CLR_CD' not in params.keys():
        # 분류, 기간별 조회 API 파라미터가 모두 빈 칸일 때
        # -> 파라미터 존재 여부에 상관 없이 명칭, 장소별 조회 API를 사용

        found_goods_list = get_response_and_convert(found_search_np_url, params)
        portal_goods_list = get_response_and_convert(portal_search_np_url, params)
    else:
        # 분류, 기간별 조회 API 파라미터가 하나라도 채워져있을 때
        # -> 파라미터 존재 여부에 상관 없이 분류, 기간별 조회 API를 사용
        # -> 단, 명칭, 장소별 조회 API 파라미터가 하나라도 있으면 습득물명 및 장소명이 결과와 일치하는지 하나씩 검사

        if 'DEP_PLACE' not in params.keys() and 'PRDT_NM' not in params.keys():
            # 명칭, 장소별 조회 API 파라미터가 모두 빈 칸일 때

            found_goods_list = get_response_and_convert(found_search_cd_url, params)
            portal_goods_list = get_response_and_convert(portal_search_cd_url, params)
        else:
            # 명칭, 장소별 조회 API 파라미터가 하나라도 채워져있을 때
            # 단, 여기서 numOfRows는 1000으로 고정한다. (디폴트값인 10으로 유지하면 속도 감소)

            page_no = 1
            max_found_candidate_num = max_portal_candidate_num = int(params['numOfRows'])
            params['numOfRows'] = 1000
            while True:
                params['pageNo'] = page_no
                candidates = get_response_and_convert(found_search_cd_url, params)
                if candidates is None:
                    break

                for candidate in candidates:
                    # 파라미터 존재 여부에 따라 습득물의 해당 파라미터와 일치하는지 검사
                    if 'DEP_PLACE' in params.keys() and 'PRDT_NM' in params.keys():
                        if params['DEP_PLACE'] in candidate['depPlace'] \
                                and params['PRDT_NM'] in candidate['fdPrdtNm']:
                            found_goods_list.append(candidate)
                            max_found_candidate_num -= 1
                    elif 'DEP_PLACE' in params.keys():
                        if params['DEP_PLACE'] in candidate['depPlace']:
                            found_goods_list.append(candidate)
                            max_found_candidate_num -= 1
                    elif 'PRDT_NM' in params.keys():
                        if params['PRDT_NM'] in candidate['fdPrdtNm']:
                            found_goods_list.append(candidate)
                            max_found_candidate_num -= 1

                    if max_found_candidate_num == 0:
                        break
                if max_found_candidate_num == 0:
                    break
                else:
                    page_no += 1

            page_no = 1
            while True:
                params['pageNo'] = page_no
                candidates = get_response_and_convert(portal_search_cd_url, params)
                if candidates is None:
                    break

                for candidate in candidates:
                    # 파라미터 존재 여부에 따라 습득물의 해당 파라미터와 일치하는지 검사
                    if 'DEP_PLACE' in params.keys() and 'PRDT_NM' in params.keys():
                        if params['DEP_PLACE'] in candidate['depPlace'] \
                                and params['PRDT_NM'] in candidate['fdPrdtNm']:
                            portal_goods_list.append(candidate)
                            max_portal_candidate_num -= 1
                    elif 'DEP_PLACE' in params.keys():
                        if params['DEP_PLACE'] in candidate['depPlace']:
                            portal_goods_list.append(candidate)
                            max_portal_candidate_num -= 1
                    elif 'PRDT_NM' in params.keys():
                        if params['PRDT_NM'] in candidate['fdPrdtNm']:
                            portal_goods_list.append(candidate)
                            max_portal_candidate_num -= 1

                    if max_portal_candidate_num == 0:
                        break
                if max_portal_candidate_num == 0:
                    break
                else:
                    page_no += 1

    # 습득물 리스트 아이템의 개수
    # (foundNumOfRows보다 작을 경우 foundNumOfRows 대신 들어갈 값)
    num_of_item = 0

    # 각 경찰서 습득물의 상세정보를 리스트에 저장
    for item in found_goods_list:
        found_goods_result = get_found_item(item, found_detail_url)
        if found_goods_result is None:
            found_goods_result = get_found_item(item, None)

        result['foundItems'].append(found_goods_result)
        num_of_item += 1

    # 리스트 아이템 개수가 foundNumOfRows보다 작다면 foundNumOfRows 갱신
    if num_of_item < int(result['foundNumOfRows']):
        result['foundNumOfRows'] = num_of_item

    # 습득물 리스트 아이템 개수 초기화
    num_of_item = 0

    # 각 포털기관 습득물의 상세정보를 리스트에 저장
    for item in portal_goods_list:
        found_goods_result = get_found_item(item, portal_detail_url)
        if found_goods_result is None:
            found_goods_result = get_found_item(item, None)

        result['portalItems'].append(found_goods_result)
        num_of_item += 1

    # 리스트 아이템 개수가 portalNumOfRows보다 작다면 portalNumOfRows 갱신
    if num_of_item < int(result['portalNumOfRows']):
        result['portalNumOfRows'] = num_of_item

    # return json.dumps(result, ensure_ascii=False)
    response = make_response(json.dumps(result, ensure_ascii=False))
    response.headers['Content-Type'] = 'application/json;charset=UTF-8'
    response.headers['mimetype'] = 'application/json'
    return response


# 해당 URL에 파라미터와 함께 요청을 보냈을 때 XML로 받은 결과를 JSON으로 변환하는 메소드
def get_response_and_convert(url, params):
    # params를 딕셔너리로 주면 서비스키 인코딩 문제 발생 (& -> %25)
    # 따라서 쿼리스트링에 파라미터를 연결하여 전달해야 함
    querystring = 'ServiceKey={0}'.format(service_key)
    for key, val in params.items():
        if val is not None:
            querystring += '&{0}={1}'.format(key, val)

    # xml 파싱 후 json 변환을 한번 거치고 딕셔너리로 변환해야
    # 파싱 데이터 내의 불필요한 요소를 제거할 수 있음
    response = requests.get(
        url=url,
        params=querystring
    )
    res_dict = xmltodict.parse(response.text)
    res_json = json.loads(json.dumps(res_dict))

    # 'response' 속성이 없는 경우(에러) None 리턴
    if 'response' in res_json.keys():
        res_item = res_json['response']['body']
    else:
        return None

    # res_item의 값이 없을 경우 None 리턴
    # print(res_item)
    if res_item is None:
        return None

    # 가지고 있는 속성에 따라 적절하게 리스트 반환
    # 해당하는 속성이 없다면 None 리턴
    if 'items' in res_item.keys():
        if res_item['items'] is not None:
            # 반환 값이 리스트이면 리스트를 리턴, 리스트가 아니면 리스트로 만들어 리턴
            if type(res_item['items']['item']) == list:
                return res_item['items']['item']
            else:
                return [res_item['items']['item']]
        else:
            return None
    elif 'item' in res_item.keys():
        return res_item['item']
    else:
        return None


# 습득물의 상세정보 리스트 아이템 객체를 반환하는 메소드
def get_found_item(item, url):
    result_obj = {}

    params_id = {
        'ATC_ID': item['atcId'],
        'FD_SN': 1
    }

    # 습득물 리스트의 상세정보를 요청
    if url is None:
        details_result = item
    else:
        details_result = get_response_and_convert(url, params_id)
        if details_result is None:
            return None

    # 각 속성의 존재 여부를 확인 후 리스트 아이템 객체에 추가
    if 'atcId' in details_result.keys():
        result_obj['id'] = details_result['atcId']

    if 'csteSteNm' in details_result.keys():
        result_obj['state'] = details_result['csteSteNm']

    if 'depPlace' in details_result.keys():
        result_obj['depPlace'] = details_result['depPlace']

    if 'fdFilePathImg' in details_result.keys():
        result_obj['image'] = details_result['fdFilePathImg']

    if 'fdHor' in details_result.keys():
        result_obj['foundHour'] = details_result['fdHor']

    if 'fdPlace' in details_result.keys():
        result_obj['foundPlace'] = details_result['fdPlace']

    if 'fdPrdtNm' in details_result.keys():
        result_obj['foundProductName'] = details_result['fdPrdtNm']

    if 'fdSn' in details_result.keys():
        result_obj['foundSeq'] = details_result['fdSn']

    if 'fdYmd' in details_result.keys():
        result_obj['foundYMD'] = details_result['fdYmd']

    if 'fndKeepOrgnSeNm' in details_result.keys():
        result_obj['foundKeepOrgCategoryName'] = details_result['fndKeepOrgnSeNm']

    if 'orgId' in details_result.keys():
        result_obj['orgId'] = details_result['orgId']

    if 'orgNm' in details_result.keys():
        result_obj['orgName'] = details_result['orgNm']

    if 'tel' in details_result.keys():
        result_obj['tel'] = details_result['tel']

    if 'uniq' in details_result.keys():
        result_obj['uniq'] = details_result['uniq']

    if 'prdtClNm' in details_result.keys():
        # 물품분류명을 상위분류명과 하위분류명으로 분리
        product_category = details_result['prdtClNm'].split(' > ')
        result_obj['productCategory'] = product_category[0]
        result_obj['productCategorySub'] = product_category[1]

    return result_obj