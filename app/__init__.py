from flask import Flask
from app.route import hello_world, index, imagePost, base64_Post
from flask_cors import CORS
def create_app():
    app = Flask(__name__)
    CORS(app)
    app.add_url_rule('/', '/', hello_world)
    app.add_url_rule('/index', 'index', index, methods=['GET'])
    app.add_url_rule('/callback', 'imagePost', imagePost, methods=['POST'])
    app.add_url_rule('/base64_Post', 'base64_Post', base64_Post, methods=['POST'])
    return app
