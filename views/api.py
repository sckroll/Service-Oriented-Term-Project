from flask import Blueprint, jsonify, json
import requests
import pprint
import xmltodict

api_blueprint = Blueprint('api', __name__)

service_key = '%2FRpRLYKrjEbwdsYlZgkvuKZW9wgTRfDhE%2BZyDgf4MzD5OcH5%2Fx92rEl1NDzjnqrHxhcYI1WUjvRfK8n86aSNaw%3D%3D'


@api_blueprint.route('/')
def api_main():
    # 1. 분실물 명칭, 보관장소 / 분류, 지역, 기간별 조회에서 atcId 추출
    # 2. 분실물 상세정보에서 상세정보 추출
    # 3. 분실물 명칭, 보관장소, 대/중분류, 색상, 검색시작일과 일치하는
    #    습득물 검색 후 atcId 추출 (포털기관도 마찬가지)
    # 4. (포털기관) 습득물 상세정보에서 상세정보 추출

    url = 'http://apis.data.go.kr/1320000/LostGoodsInfoInqireService/getLostGoodsInfoAccTpNmCstdyPlace'

    # params를 딕셔너리로 주면 서비스키 인코딩 문제 발생 (& -> %25)
    res_lost_goods = requests.get(
        url=url,
        params='ServiceKey={0}'.format(service_key)
        + '&LST_PLACE={0}&LST_PRDT_NM={1}'.format('', '지갑')
        + '&pageNo={0}&numOfRows={1}'.format(1, 10)
    )
    response_dict = xmltodict.parse(res_lost_goods.text, encoding=None)
    response_json = json.dumps(response_dict)
    results = json.loads(response_json)

    res_json = {}
    res_item = {}

    res_json['items'] = []
    res_json['items'].append(res_item)
    res_json['lostPageNo'] = 0
    res_json['lostNumOfRows'] = 0
    res_json['relatedPageNo'] = 0
    res_json['relatedNumOfRows'] = 0

    return results
