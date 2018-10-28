# imports application module from app directory
from app import app

# base webpage
@app.route('/')
@app.route('/home')
def home():
    return "This is the home webpage"
