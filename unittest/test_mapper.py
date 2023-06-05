
from mapped_haystack.mapper import Haystack2Brick
from dotenv import load_dotenv




def test_queries():
    load_dotenv()
    hb = Haystack2Brick()

    run_classes = hb.tags2classes({'run'})
    assert len(run_classes) > 1

    nonexisting_classes = hb.tags2classes({'nonexisting'})
    assert not nonexisting_classes

