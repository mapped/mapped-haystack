
from typing import Set, List
from pdb import set_trace as bp
import os
import pandas as pd


class Haystack2Brick(object):

    def __init__(self):
        self.init_raw_mapping()

    def init_raw_mapping(self):
        df = pd.read_csv(os.environ["HAYSTACK_BRICK"])
        df['haystack_tags'] = df["Haystack:Markers"].str.split(', ', regex=False)
        df['haystack_tags'] = df.apply(lambda row: set(row['haystack_tags']) if isinstance(row['haystack_tags'], list) else set(), axis=1)
        self.mapping = df

    def tags2classes(self, query_htags: Set[str]):

        def is_in(htags):
            if query_htags.issubset(htags):
                return True
            else:
                return False

        filter = self.mapping['haystack_tags'].apply(is_in)
        filtered = self.mapping['Brick:PointClass'].loc[filter]
        klasses = set(filtered.values)
        return klasses




if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()
    hb = Haystack2Brick()

    hb.tags2classes(['run'])
