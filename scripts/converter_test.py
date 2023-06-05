from mapped_haystack.mapped import GraphqlBuilder, GraphqlClient
from mapped_haystack.convert import QueryConverter
from mapped_haystack.haystack import GridBuilder
from pdb import set_trace as bp
from dotenv import load_dotenv




def main():
    load_dotenv()

    gql_builder = GraphqlBuilder()
    converter = QueryConverter()

    gql_cli = GraphqlClient()


    #Get all points
    """
    qstr = "temp and air"
    query = converter.haystack2mapped(qstr)
    res = gql_cli.execute(query)
    print(res)
    bp()
    """

    # Query for a VAV
    qstr = "temp and air and equipRef == @THGR74JdyPzYoAsdbWcaZiUgG"
    query = converter.haystack2mapped(qstr)
    res = gql_cli.execute(query)
    print(res)

    """
    qstr = "temp and air and siteRef == @BLDG5o26DguWKu5T9nRvSYn5Em"
    query = converter.haystack2mapped(qstr)
    res = gql_cli.execute(query)
    print(res)
    bp()
    """


    grid_builder = GridBuilder()
    grid = grid_builder.gql_to_grid(res)
    print(grid)
    bp()

    print('done')


if __name__ == '__main__':
    main()
