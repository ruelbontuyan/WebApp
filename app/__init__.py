from flask import Flask
from models import *

app = Flask(__name__)
app.static_folder = 'static'

from app import controller
