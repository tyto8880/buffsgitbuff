from flask import Flask
from config import Config

# creates new app instance
app = Flask(__name__)
# loads configuration vars
app.config.from_object(Config)

# opens up different directory routes for webpage e.g. http//.../route
from app import routes
