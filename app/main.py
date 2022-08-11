
from airline import Airline
from adsb import Adsb
from enrich import Enrich
import sys


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "loaddb":
            Airline().load_data()
            Enrich().enrich_pipeline()
        else:
            Adsb().main()
    else:
        Adsb().main()

if __name__ == '__main__':
	main()
