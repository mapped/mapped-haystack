
from functools import reduce
from flask import Flask, request, Response
from pdb import set_trace as bp
from shaystack.zincparser import parse_grid
from shaystack.zincdumper import dump_grid

from .convert import QueryConverter
from .haystack import GridBuilder
from .mapped import GraphqlClient


app = Flask(__name__)





@app.post('/haystack/read')
def read():
    gql_cli = GraphqlClient()
    converter = QueryConverter()
    grid_builder = GridBuilder()

    body = request.data.decode('utf-8')

    req_grid = parse_grid(body)

    grids = []
    if 'filter' in req_grid.column:
        for row in req_grid:
            filter_str = row['filter']
            query = converter.haystack2mapped(filter_str)
            res = gql_cli.execute(query)
            grids.append(grid_builder.gql_to_grid(res))
    grid = reduce(lambda x,y: x+y, grids)
    resp = Response(dump_grid(grid))
    resp.headers['Content-Type'] = "text/zinc; charset=utf-8"
    return resp
    bp()

    return











