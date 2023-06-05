
from typing import List, Optional, Set
import requests
import time
from pdb import set_trace as bp
from gql import Client
from gql.dsl import DSLSchema, dsl_gql, DSLQuery
from gql.transport.aiohttp import AIOHTTPTransport
import os

from .mapper import Haystack2Brick


class TokenCache(object):
    def __init__(self, token: str):
        self.token = "Bearer " + token

    def get_token(self) -> str:
        return self.token

class PAT(object):
    def __init__(self, token: str):
        self.token = "token " + token
    def get_token(self):
        return self.token


class AuthHandler(object):
    def __init__(self, client_id, client_secret, auth_domain, api_identifier):
        self.client_id = client_id
        self.client_secret = client_secret
        self.auth_domain = auth_domain
        self.auth_url = f"https://{self.auth_domain}/oauth/token"
        self.api_identifier = api_identifier
        self.payload = f"grant_type=client_credentials&client_id={self.client_id}&client_secret={self.client_secret}&audience={self.api_identifier}"
        self.headers = {"content-type": "application/x-www-form-urlencoded"}
        self.expires_at = time.time()  # unix timestamp

    def get_token(self):
        if self.expires_at < time.time() + 60:
            self.renew_token()
        return self.token

    def renew_token(self):
        resp = requests.post(self.auth_url, data=self.payload, headers=self.headers)
        res = resp.json()
        self.token = "Bearer " + res["access_token"]
        self.expires_at = time.time() + res["expires_in"]


class GraphqlClient(object):
    def __init__(self):
        api_endpoint = "{0}://{1}:{2}/graphql".format(
            os.environ["MAPPED_CORE_GRAPHQL_SCHEME"],
            os.environ["MAPPED_CORE_GRAPHQL_HOSTNAME"],
            os.environ["MAPPED_CORE_GRAPHQL_PORT"],
        )
        auth_handler = PAT(
            os.environ["PAT"],
        )
        org_id = "ORGUmvDdxfFU7UBvJ8Msx2A6J" #TODO: impl: set_org_id
        headers = {
            "content-type": "application/json",
            "X-Mapped-Org-Id": org_id,
        }
        headers["Authorization"] = auth_handler.get_token()
        transport = AIOHTTPTransport(url=api_endpoint, headers=headers)
        self.client = Client(transport=transport, fetch_schema_from_transport=True)


    def execute(self, query):
        return self.client.execute(query)


class GraphqlBuilder(object):

    def __init__(self):
        self.init_schema()

        self.tags: Optional[Set] = None
        self.equip_refs = []
        self.site_ref = None
        self.air_ref = None
        self.hb = Haystack2Brick()

    def add_site_ref(self, site_ref):
        assert not self.site_ref or self.site_ref == site_ref, "A single site ref is supoprted for now."
        self.site_ref = site_ref

    def add_equip_ref(self, equip_ref):
        self.equip_refs.append(equip_ref)

    def add_tag(self, tag):
        if self.tags is None:
            self.tags = set()
        self.tags.add(tag)

    def init_schema(self):
        schema_file = os.environ["GRAPHQL_SCHEMA"]
        client = Client(schema=open(schema_file).read())
        self.ds = DSLSchema(client.schema)

        self.default_thing_select_args = [
            self.ds.Thing.id,
            self.ds.Thing.name,
        ]
        self.default_point_select_args = [
            self.ds.Point.id,
            self.ds.Point.name,
            self.ds.Point.series.args(latest=True).select(
                self.ds.TimeseriesRow.timestamp,
                self.ds.TimeseriesRow.value.select(self.ds.TimeseriesRowValue.float64Value)
            )
        ]

    def points_query(self, parent=None, point_types: Optional[List[str]]=None):
        """
        `parent` may be `self.ds.Query`
        """
        if self.site_ref:
            building_query = self.ds.Query.buildings(filter={"id": {"eq": self.site_ref}})
        else:
            building_query = self.ds.Query.buildings()

        if self.equip_refs:
            assert len(self.equip_refs) == 1, "Are multiple equipRefs allowed for points?"
            equip_ref = self.equip_refs[0]
            thing_query = self.ds.Building.things(filter={'id': {'eq': equip_ref}})
        else:
            thing_query = self.ds.Building.things()

        top_selector = building_query.select(thing_query)

        if self.tags is None:
            point_query = self.ds.Thing.points()
        else:
            point_types = self.hb.tags2classes(self.tags)
            point_query = self.ds.Thing.points(
                filter={"type": {"in": point_types}}
            )

        point_selector = point_query.select(*self.default_point_select_args)
        thing_query.select(point_selector)
        query = DSLQuery(top_selector )
        return dsl_gql(query)

    def things_query(self, parent=None, thing_types: Optional[List[str]]=None):
        """
        `parent` may be `self.ds.Query`
        """
        if not parent:
            parent = self.ds.Query
        if thing_types is None:
            base = parent.things()
        else:
            base = parent.things(
                filter={"type": {"in": thing_types}}
            )
        selector = base.select(*self.default_thing_select_args)

        query = DSLQuery(selector)
        return dsl_gql(query)

