from flask import Flask

# creates new app instance
app = Flask(__name__)

# opens up different directory routes for webpage e.g. http//.../route
from app import routes
