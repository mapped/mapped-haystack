
from dotenv import load_dotenv
from mapped_haystack.mapped import GraphqlBuilder



def test_gen():
    load_dotenv()
    builder = GraphqlBuilder()
    builder.points_query()
