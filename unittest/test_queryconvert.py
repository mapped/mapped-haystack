
from dotenv import load_dotenv


from mapped_haystack.convert import QueryConverter


def test_queries():
    load_dotenv()

    converter = QueryConverter()
    qstr = "point and temp and siteRef==@siteA"

    res = converter.haystack2mapped(qstr)
    print(res)




