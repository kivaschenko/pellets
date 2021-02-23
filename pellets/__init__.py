import os
from flask import Flask


def create_app(test_config=None):
    '''Create and configure the app'''
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='development',
        CSRF_TOKEN='somecsrftoketfordebugonly',
        DEBUG=True
    )
    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db 
    db.init_app(app)

    from . import auth 
    app.register_blueprint(auth.bp)

    from . import offer
    app.register_blueprint(offer.bp)

    app.add_url_rule('/', endpoint='home')
    return app