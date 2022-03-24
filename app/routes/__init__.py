from flask import Flask
from .series_routes import series_routes

def init_app(app: Flask):
    
    series_routes(app)