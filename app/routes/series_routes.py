from flask import Flask

def series_routes(app: Flask):

    @app.get('/series')
    def get_all_series():
        return {'msg': 'all series'}

    @app.get('/series/<serie_id>')
    def get_series(serie_id):
        return {'msg': f'got serie from id {serie_id}'}

    @app.post('/series')
    def add_serie():
        return {'msg': 'serie added'}