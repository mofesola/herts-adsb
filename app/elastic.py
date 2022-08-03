from elasticsearch import Elasticsearch
import os
import json


class Elastic:
    def __init__(self, host, port) -> None:
        self.host = os.getenv('ES_HOST', '127.0.0.1')
        self.port = os.getenv('ES_PORT', '9200')

    def es(self):
        return Elasticsearch(self.host, self.port)
    
    def mappings(self):
        f = open('config/mapping.json')
        return json.load(f)

    def create_index(self):
        response = self.es().indices.create(
            index="herts_adsb",
            body=self.mappings,
            ignore=400
        )

        print(response)

        if 'acknowledged' in response:
            if response['acknowledged'] == True:
                print("INDEX MAPPING SUCCESS FOR INDEX:", response['index'])
                return True

            elif 'error' in response:
                print ("ERROR:", response['error']['root_cause'])
                print ("TYPE:", response['error']['type'])
                return False
