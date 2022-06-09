from flask import Flask
from . import item

__version__ = "0.1.0"

app = Flask(__name__)
app.register_blueprint(item.bp, url_prefix="/item")
