import os

from flask import Flask, render_template, request
from flask_restful import Api
import logging

from database import base
from database.base import User
from flask_login import current_user, LoginManager

from views.menus import menu_blueprint
from views.auth import auth_blueprint
from rest_server.resource_check import resource_blueprint
from rest_server.resource import TemperatureResource, TemperatureCreationResource, TemperatureByLocationResource

from views.api import api_blueprint


application = Flask(__name__)
application.register_blueprint(menu_blueprint, url_prefix='/menu')
application.register_blueprint(auth_blueprint, url_prefix='/auth')
application.register_blueprint(resource_blueprint, url_prefix='/resource_check')

application.register_blueprint(api_blueprint, url_prefix='/api')

api = Api(application)
api.add_resource(TemperatureResource, '/resource/<sensor_id>')
api.add_resource(TemperatureCreationResource, '/resource_creation')
api.add_resource(TemperatureByLocationResource, '/resource/location/<location>')


application.config['WTF_CSRF_SECRET_KEY'] = os.urandom(24)
application.config['SECRET_KEY'] = os.urandom(24)

login_manager = LoginManager()
login_manager.init_app(application)


@login_manager.user_loader
def load_user(user_id):
    q = base.db_session.query(User).filter(User.id == user_id)
    user = q.first()

    if user is not None:
        user._authenticated = True
    return user


@application.errorhandler(404)
def page_not_found(error):
    application.logger.error(error)
    return "<h1>응 404~</h1>", 404


@application.route('/')
def hello_world():
    # html file은 templates 폴더에 위치해야 함
    return render_template(
        'index.html',
        nav_menu="home",
        current_user=current_user
    )


@application.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        myName = request.form['myName']
    else:
        myName = request.args.get('myName')
    # return 'Welcome, %s' % myName
    return 'Welcome, {0}'.format(myName)


@application.route('/message/<int:msg_id>')
def get_message(msg_id):
    return 'message id: %d' % msg_id


if __name__ == '__main__':
    # 로그로 남기기 위해 filename='test.log' parameter로 넘길 것
    logging.basicConfig(filename='test.log', level=logging.DEBUG)

    # AWS에 배포할 때에는 application.debug를 False로 바꿀 것
    application.debug = True
    application.run(host="localhost", port="8000")
