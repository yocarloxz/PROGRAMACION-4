from flask import Flask
from flask_restful import Api
from .routes import BookListResource, BookResource
from .config import Config
import redis

app = Flask(__name__)
app.config.from_object(Config)
api = Api(app)

# Redis connection
r = redis.Redis(host=app.config['REDIS_HOST'], port=app.config['REDIS_PORT'], decode_responses=True)

# Add RESTful resources
api.add_resource(BookListResource, '/books')
api.add_resource(BookResource, '/books/<string:book_id>')
