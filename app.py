from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

debug = DebugToolbarExtension(app)


@app.route('/')
def home_page():
    return 'home'
    

