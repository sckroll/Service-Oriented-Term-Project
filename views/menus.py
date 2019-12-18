from flask import Blueprint, render_template, request
import requests
import pprint

from views.api import service_key

LOST_BASE_URL = 'http://localhost:8000/api/lostInfo'
FOUND_BASE_URL = 'http://localhost:8000/api/foundInfo'
menu_blueprint = Blueprint('menu', __name__)


@menu_blueprint.route('/api_run')
def api_run():
    querystring = '&{0}={1}' .format('getPredictedItems', 0)
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
    querystring =''
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


@menu_blueprint.route('/lost_search', methods=['GET', 'POST'])
def api_example():

    return render_template(
       'lost_search.html', nav_menu="lost_search"
    )


@menu_blueprint.route('/found_search', methods=['GET', 'POST'])
def api_example2():

    return render_template(
       'found_search.html', nav_menu="found_search"
    )


@menu_blueprint.route('/lost_result', methods=['GET', 'POST'])
def lost_result():
    querystring = ""
    if request.method == 'POST':
        result = request.form
        p_search = 1
        for key, val in result.items():
            if val == 'on':
                querystring += '&{0}={1}' .format(key, 0)
                p_search = 0
            elif val != "":
                querystring += '&{0}={1}'.format(key, val)
        print(querystring[:-10])
        res1 = requests.get(
            url=LOST_BASE_URL,
            params=querystring[:-10]
        )
        if res1.status_code == 200:
            lostThings = res1.json()
        for item in lostThings['items']:
            pprint.pprint(item)
    return render_template(
        'lost_result.html',
        nav_menu="lost_search",
        result = result,
        lostThings=lostThings,
        p_search=p_search
    )


@menu_blueprint.route('/found_result', methods=['GET', 'POST'])
def found_result():
    querystring = ""
    if request.method == 'POST':
        result = request.form
        for key, val in result.items():
            if val != '':
                querystring += '&{0}={1}'.format(key, val)
        print(querystring[:-10])
        res1 = requests.get(
            url=FOUND_BASE_URL,
            params=querystring[:-10]
        )
        if res1.status_code == 200:
            foundThings = res1.json()
        for item in foundThings['foundItems']:
            pprint.pprint(item)
        for item in foundThings['portalItems']:
            pprint.pprint(item)
    return render_template(
        'found_result.html',
        nav_menu="found_search",
        result = result,
        foundThings=foundThings
    )


@menu_blueprint.route('/lost_return', methods=['GET', 'POST'])
def lost_return():
    if request.method == 'POST':
        return render_template('lost_search.html', nav_menu="api_example")


@menu_blueprint.route('/found_return', methods=['GET', 'POST'])
def found_return():
    if request.method == 'POST':
        return render_template('found_search.html', nav_menu="api_example2")