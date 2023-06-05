from functools import reduce
from pdb import set_trace as bp

from shaystack import Grid
from shaystack.datatypes import Ref
from typing import List, Dict


def adder(x, y):
    return x + y

def get_latest(point):
    value = None
    if point['series']:
        value = point["series"][-1]["value"]["float64Value"]
    return value

class GridBuilder(object):
    def __init__(self):

        self.grid2gql_mappings = {
            "id": lambda point: Ref(name=point["id"]),
            "dis": lambda point: point["name"],
            "curVal": get_latest
        }

    def gql_to_grid(self, gql_result: List[Dict]):
        grid = Grid(columns=list(self.grid2gql_mappings.keys()))
        things = reduce(adder, [building['things'] for building in gql_result["buildings"]])
        points = reduce(adder, [thing["points"] for thing in things])
        for row in points:
            grid.append({k: mapping(row) for k, mapping in self.grid2gql_mappings.items()})
        return grid

