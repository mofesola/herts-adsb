from operator import index
from unicodedata import name
from elasticsearch import Elasticsearch
import elasticsearch
import json
from common import Common

class Enrich:
    def __init__(self) -> None:
        self.host = Common().es_host()
        self.port = Common().es_port()
        self.index = Common().es_airline_index()
        self.policy_name = 'add_airline_data'
        self.es = Elasticsearch('http://'+self.host+':'+self.port, timeout=30, max_retries=10, retry_on_timeout=True)
    
    
    def enrich_pipeline(self):
        try:
            self.create_policy()
            self.execute_policy()
            self.create_pipeline()
        except elasticsearch.ApiError as error:
            print(error)

    def create_policy(self):
        if self.es.enrich.get_policy(name=self.policy_name)['policies'] == []:
            return self.es.enrich.put_policy(
                name=self.policy_name,
                match={
                    'indices' : self.index,
                    'match_field' : 'hex_ident',
                    'enrich_fields' : [
                        'registration',
                        'manufacturer',
                        'icao_manufacturer',
                        'model',
                        'icao_model',
                        'serial_number',
                        'line_number',
                        'icao_classification',
                        'owner',
                        'airline_callsign',
                        'airline_icao',
                        'airline_iata',
                        'operator',
                        'comments'
                    ]
                }
            )

    
    def execute_policy(self):
        return self.es.enrich.execute_policy(
            name=self.policy_name
            )

    def create_pipeline(self):
        return self.es.ingest.put_pipeline(
            id=1,
            description='Enrich data coming from ADSB with Airline and Aircraft information',
            processors=[
                {
                    'enrich': {
                        'policy_name': self.policy_name,
                        'field': 'hex_ident',
                        'target_field': 'airline_data',
                        'max_matches': 1
                    }
                }
            ]
        )
