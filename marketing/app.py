from flask import Flask
from handler import Handler
import sys

sys.path.insert(0, '../')
# from config import *

app = Flask(__name__)
app_context = app.app_context()
app_context.push()

Handler.escuchar()
