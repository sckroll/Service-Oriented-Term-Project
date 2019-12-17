from flask import Blueprint, render_template, request
import requests
import pprint

from forms import LostData
from keys import KAKAO_REST_KEY
from views.api import service_key

KAKAO_BASE_URL = 'https://dapi.kakao.com'
headers = {'Authorization': 'KakaoAK ' + KAKAO_REST_KEY}

LOST_BASE_URL = 'http://localhost:8000/api/lostInfo'
FOUND_BASE_URL = 'http://localhost:8000/api/foundInfo'
menu_blueprint = Blueprint('menu', __name__)


@menu_blueprint.route('/')
def menu_main():
    return 'Welcome news {0}'.format('SCK')

#
# @menu_blueprint.route('/images')
# def images():
#     query = '떼껄룩'
#     res2 = requests.get(
#        url=KAKAO_BASE_URL + "/v2/search/image?query=" + query,
#        headers=headers
#     )
#     if res2.status_code == 200:
#        docs = res2.json()
#        pprint.pprint(docs)
#
#        images = []
#        for image in docs['documents']:
#            images.append(image['image_url'])
#     else:
#        print("Error {0}".format(res2.status_code))
#
#     return render_template(
#        'images.html', nav_menu="image", images=images
#     )
#
#
# @menu_blueprint.route('/books')
# def books():
#     query = '미움받을 용기'
#     res2 = requests.get(
#        url=KAKAO_BASE_URL + "/v3/search/book?target=title&query=" + query,
#        headers=headers
#     )
#     if res2.status_code == 200:
#        books = res2.json()
#
#        for book in books['documents']:
#            print("{0:50s}-{1:20s}".format(book['title'], str(book['authors'])))
#     else:
#        print("Error {0}".format(res2.status_code))
#
#     return render_template(
#        'books.html', nav_menu="book", books=books
#     )


@menu_blueprint.route('/api_run')
def api_run():
    querystring = ''
    res1 = requests.get(
       url= LOST_BASE_URL,
       params=querystring
    )
    if res1.status_code == 200:
       lostThings = res1.json()

       for item in lostThings['items']:
           pprint.pprint(item)
    else:
       print("Error {0}".format(res1.status_code))

    res2 = requests.get(
        url= FOUND_BASE_URL,
        params=querystring
    )
    if res2.status_code == 200:
        foundThings = res2.json()

        for item in foundThings['foundItems']:
            pprint.pprint(item)
        for item in foundThings['portalItems']:
            pprint.pprint(item)
    return render_template(
       'api_run.html',
        nav_menu="api_run",
        lostThings=lostThings,
        foundThings=foundThings,
    )


@menu_blueprint.route('/api_manual')
def api_manual():


    return render_template(
       'api_manual.html', nav_menu="api_manual"
    )


@menu_blueprint.route('/api_example', methods=['GET', 'POST'])
def api_example():

    return render_template(
       'api_example.html', nav_menu="api_example"
    )


@menu_blueprint.route('/api_result', methods=['GET', 'POST'])
def result():
    #querystring ="ServiceKey={0}" .format(service_key)
    querystring = ""
    if request.method == 'POST':
        result = request.form

        for key, val in result.items():
            if val == 'on':
                querystring += '&{0}={1}' .format(key, 1)
            elif val is not None:
                querystring += '&{0}={1}'.format(key, val)
        print(querystring[:-14])
        res1 = requests.get(
            url=LOST_BASE_URL,
            params=querystring[:-14]
        )
        if res1.status_code == 200:
            lostThings = res1.json()
        for item in lostThings['items']:
            pprint.pprint(item)
    return render_template(
        'api_result.html',
        nav_menu="api_example",
        result = result,
        lostThings=lostThings
    )


@menu_blueprint.route('/api_return', methods=['GET', 'POST'])
def api_return():
    if request.method == 'POST':
        return render_template('api_example.html', nav_menu="api_example")