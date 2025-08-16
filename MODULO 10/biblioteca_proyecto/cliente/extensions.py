from flask_bootstrap import Bootstrap
from flask_wtf import CSRFProtect
from flask_moment import Moment

bootstrap = Bootstrap()
csrf = CSRFProtect()
moment = Moment()

def init_extensions(app):
    bootstrap.init_app(app)
    csrf.init_app(app)
    moment.init_app(app)

