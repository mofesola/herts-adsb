import os
class Common:
    
    def __init__(self):
        pass

    def host(self):
        return os.getenv('HOST', 'piaware.local')

    def port(self):
        return int(os.getenv('PORT', 30003))

    def es_host(self):
        return os.getenv('ES_HOST', 'localhost')

    def es_port(self):
        return os.getenv('ES_PORT', '9200')

    def es_index(self):
        return os.getenv('ES_INDEX', 'herts_adsb')

    def buffer_size(self):
        return int(os.getenv('BUFFER_SIZE', 100))

    def batch_size(self):
        return int(os.getenv('BATCH_SIZE', 1))
    
    def connect_attempt_limit(self):
        return int(os.getenv('CONNECT_ATTEMPT_LIMIT', 10))

    def connect_attempt_delay(self):
        return int(os.getenv('CONNECT_ATTEMPT_DELAY', 5))

    def log_config(self):
        print(
            self.host(), '\n',
            self.port(), '\n',
            self.es_host(), '\n',
            self.es_port(), '\n',
            self.es_index(), '\n',
            self.buffer_size(), '\n',
            self.batch_size(), '\n',
            self.connect_attempt_limit(), '\n',
            self.connect_attempt_delay(), '\n',
        )

