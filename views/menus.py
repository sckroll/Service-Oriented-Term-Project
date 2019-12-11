from flask import Blueprint, render_template
import requests
import pprint
from keys import KAKAO_REST_KEY

KAKAO_BASE_URL = 'https://dapi.kakao.com'
headers = {'Authorization': 'KakaoAK ' + KAKAO_REST_KEY}


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
       'images.html', images=images
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
       'books.html', books=books
    )
