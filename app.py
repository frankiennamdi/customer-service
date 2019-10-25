import flask_cors
from flask import Flask, jsonify

from services.local_pay_co_data_service import LocalPayCoDataService
from views import health_check
from views.model import schema
from views.customer_graphql import CustomerGraphQl

cors = flask_cors.CORS()


def create_app():
    app = Flask(__name__)
    cors.init_app(app)
    app.debug = True

    app.register_blueprint(health_check.blueprint, url_prefix='/api')

    app.add_url_rule('/api/customer',
                     view_func=CustomerGraphQl.as_view("customer-api", LocalPayCoDataService('resources/data'),
                                                       schema=schema, batch=True, graphiql=True))

    @app.errorhandler(404)
    def page_not_found(e):
        return jsonify({'message': 'Endpoint Resource Not Found.'}), 404

    return app
