from flask import Blueprint, render_template
import requests
import pprint
from keys import KAKAO_REST_KEY, OPEN_API_SERVICE_KEY



KAKAO_BASE_URL = 'https://dapi.kakao.com'
headers = {'Authorization': 'KakaoAK ' + KAKAO_REST_KEY}


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



menu_blueprint = Blueprint('menu', __name__)


@menu_blueprint.route('/')
def menu_main():
    return 'Welcome news {0}'.format('SCK')


@menu_blueprint.route('/images')
def images():
    query = '떼껄룩'
    res2 = requests.get(
       url=KAKAO_BASE_URL + "/v2/search/image?query=" + query,
       headers=headers
    )
    if res2.status_code == 200:
       docs = res2.json()
       pprint.pprint(docs)

       images = []
       for image in docs['documents']:
           images.append(image['image_url'])
    else:
       print("Error {0}".format(res2.status_code))

    return render_template(
       'images.html', nav_menu="image", images=images
    )


@menu_blueprint.route('/books')
def books():
    query = '미움받을 용기'
    res2 = requests.get(
       url=KAKAO_BASE_URL + "/v3/search/book?target=title&query=" + query,
       headers=headers
    )
    if res2.status_code == 200:
       books = res2.json()

       for book in books['documents']:
           print("{0:50s}-{1:20s}".format(book['title'], str(book['authors'])))
    else:
       print("Error {0}".format(res2.status_code))

    return render_template(
       'books.html', nav_menu="book", books=books
    )


@menu_blueprint.route('/api_run')
def api_run():
    query = '미움받을 용기'
    res2 = requests.get(
       url=KAKAO_BASE_URL + "/v3/search/book?target=title&query=" + query,
       headers=headers
    )
    if res2.status_code == 200:
       books = res2.json()

       for book in books['documents']:
           print("{0:50s}-{1:20s}".format(book['title'], str(book['authors'])))
    else:
       print("Error {0}".format(res2.status_code))

    return render_template(
       'api_run.html', nav_menu="api_run", books=books
    )


@menu_blueprint.route('/api_manual')
def api_manual():
    query = '미움받을 용기'
    res2 = requests.get(
       url=KAKAO_BASE_URL + "/v3/search/book?target=title&query=" + query,
       headers=headers
    )
    if res2.status_code == 200:
       books = res2.json()

       for book in books['documents']:
           print("{0:50s}-{1:20s}".format(book['title'], str(book['authors'])))
    else:
       print("Error {0}".format(res2.status_code))

    return render_template(
       'api_manual.html', nav_menu="api_manual", books=books
    )


@menu_blueprint.route('/api_example')
def api_example():
    query = '미움받을 용기'
    res2 = requests.get(
       url=KAKAO_BASE_URL + "/v3/search/book?target=title&query=" + query,
       headers=headers
    )
    if res2.status_code == 200:
       books = res2.json()

       for book in books['documents']:
           print("{0:50s}-{1:20s}".format(book['title'], str(book['authors'])))
    else:
       print("Error {0}".format(res2.status_code))

    return render_template(
       'api_example.html', nav_menu="api_example", books=books
    )
