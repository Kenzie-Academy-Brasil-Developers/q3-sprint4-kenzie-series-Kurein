from http import HTTPStatus
from flask import Flask, request
from app.models import Series
from psycopg2.errors import UndefinedTable

def series_routes(app: Flask):

    @app.get('/series')
    def series():
        class_init = Series()
        return class_init.all_series()

    @app.get('/series/<serie_id>')
    def select_by_id(serie_id):
        class_init = Series()
        try:
            return class_init.get_by_id(serie_id)
        except (TypeError, UndefinedTable):
            return {}, HTTPStatus.NOT_FOUND

    @app.post('/series')
    def create():
        class_init = Series()
        data = request.get_json()
        return class_init.create_serie(data)