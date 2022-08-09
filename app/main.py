
from airline import Airline
from adsb import Adsb
from enrich import Enrich

def main():
    Airline().load_data()
    Enrich().enrich_pipeline()
    Adsb().main()

if __name__ == '__main__':
	main()
