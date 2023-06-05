import shaystack
from shaystack.grid_filter import parse_filter

from pdb import set_trace as bp


from .mapped import GraphqlBuilder


def has_op(gql_builder, node):
    assert len(node.right.paths) == 1
    assert node.operator == "has"
    htag = node.right.paths[0]
    gql_builder.add_tag(htag)

def and_op(gql_builder, node):
    base_op(gql_builder, node.left)
    base_op(gql_builder, node.right)

def get_ref_id(ref: shaystack.datatypes.Ref):
    assert isinstance(ref, shaystack.datatypes.Ref)
    return ref.name

def eq_op(gql_builder, node):
    if node.left.paths[0] == "siteRef":
        gql_builder.add_site_ref(get_ref_id(node.right))
    elif node.left.paths[0] == "equipRef":
        gql_builder.add_equip_ref(get_ref_id(node.right))
    else:
        raise NotImplementedError(f"eq not fully implemented: {node}")

def base_op(gql_builder, node):
    if node.operator == "has":
        has_op(gql_builder, node)
    elif node.operator == "and":
        and_op(gql_builder, node)
    elif node.operator == "or":
        raise NotImplementedError(f"or op not implemented yet: {node}")
    elif node.operator == "==":
        eq_op(gql_builder, node)
    else:
        print(node)
        raise NotImplementedError(f"TODO: {node}")

class QueryConverter(object):

    """
    currently doesn't support `or` operation in haystack filters
    """

    def __init__(self):
        pass


    def haystack2mapped(self, haystack_filter):
        gql_builder = GraphqlBuilder()
        filter_ast = parse_filter(haystack_filter)
        node = filter_ast.head

        base_op(gql_builder, node)

        query = gql_builder.points_query()
        return query





