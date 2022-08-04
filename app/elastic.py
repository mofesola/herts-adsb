from elasticsearch import Elasticsearch 
import elasticsearch
import json
from common import Common

class Elastic:
    def __init__(self) -> None:
        self.host = Common().es_host()
        self.port = Common().es_port()
        self.index = Common().es_index()
        self.es = Elasticsearch(self.host+':'+self.port, timeout=30, max_retries=10, retry_on_timeout=True)
    
    def mappings(self):
        f = open('config/mapping.json')
        return json.load(f)

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
        data_map["message_type"] = data[0]
        data_map["transmission"] = data[1]
        data_map["session_id"] = data[2]
        data_map["aircraft_id"] = data[3]
        data_map["hex_ident"] = data[4]
        data_map["flight_id"] = data[5]
        data_map["generated_date"] = data[6]
        data_map["generated_time"] = data[7]
        data_map["logged_date"] = data[8]
        data_map["logged_time"] = data[9]
        data_map["callsign"] = data[10]
        data_map["altitude"] = data[11]
        data_map["ground_speed"] = data[12]
        data_map["track"] = data[13]
        data_map["location"] = {"lat": float(data[14]), "lon" : float(data[15])}
        data_map["vertical_rate"] = data[16]
        data_map["squawk"] = data[17]
        data_map["alert"] = data[18]
        data_map["emergency"] = data[19]
        data_map["spi"] = data[20]
        data_map["is_on_ground"] = data[21]
        data_map["parsed_time"] = data[22]

        print(data_map)
        
        return data_map