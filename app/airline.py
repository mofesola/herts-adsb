from elasticsearch import Elasticsearch 
import elasticsearch
import json
from common import Common

class Airline:
    def __init__(self) -> None:
        self.host = Common().es_host()
        self.port = Common().es_port()
        self.index = Common().es_airline_index()
        self.es = Elasticsearch('http://'+self.host+':'+self.port, timeout=30, max_retries=10, retry_on_timeout=True)
    
    def mappings(self):
        f = open('config/aircraftdb-mapping.json')
        return json.load(f)
    
    def aircraftdb(self):
        f = open('dataset/aircraftdb.csv', 'r', encoding='utf-8')
        return f.readlines()
    
    def load_data(self):
        self.create_index()
        if self.index_size() < 450000:
            for line in self.aircraftdb():
                es_object = self.format([x.strip('\"') for x in line.strip().split(',')])
                self.insert(es_object)

    def create_index(self):
        if not self.es.indices.exists(index=self.index):
            response = self.es.indices.create(
                index=self.index,
                body=self.mappings(),
                ignore=400
            )

            if 'acknowledged' in response:
                if response['acknowledged'] == True:
                    print("INDEX MAPPING SUCCESS FOR INDEX:", response['index'])
                    return True

                elif 'error' in response:
                    print ("ERROR:", response['error']['root_cause'])
                    print ("TYPE:", response['error']['type'])
                    return False

        return True

    def index_size(self):
        return int(self.es.cat.count(index=self.index, params={"format": "json"})[0]['count'])

    def insert(self, data):
        if self.create_index():
            try:
                response = self.es.index(index=self.index, body=data)
            except elasticsearch.ElasticsearchException as es1:
                print(es1)
                return False
        
        return response
            

    def format(self, data):
        data_map = {}
        data_map["hex_ident"] = data[0].upper()
        data_map["registration"] = data[1]
        data_map["manufacturer"] = data[2]
        data_map["icao_manufacturer"] = data[3]
        data_map["model"] = data[4]
        data_map["icao_model"] = data[5]
        data_map["serial_number"] = data[6]
        data_map["line_number"] = data[7]
        data_map["icao_classification"] = data[8]
        data_map["owner"] = data[9]
        data_map["airline_callsign"] = data[10]
        data_map["airline_icao"] = data[11]
        data_map["airline_iata"] = data[12]
        data_map["operator"] = data[13]
        data_map["comments"] = data[13]
        
        print(data_map)
        
        return data_map
