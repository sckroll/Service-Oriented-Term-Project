from flask import Flask, render_template
from flask_restful import Api

from views.menus import menu_blueprint
from views.api import api_blueprint


application = Flask(__name__)
application.register_blueprint(menu_blueprint, url_prefix='/menu')
application.register_blueprint(api_blueprint, url_prefix='/api')

api = Api(application)


@application.errorhandler(404)
def page_not_found(error):
    application.logger.error(error)
    return "<h1>응 404~</h1>", 404


@application.route('/')
def hello_world():
    # html file은 templates 폴더에 위치해야 함
    return render_template('index.html')


if __name__ == '__main__':
    # AWS에 배포할 때에는 application.debug를 False로 바꿀 것
    application.debug = True
    application.run(host="0.0.0.0", port="8000")
