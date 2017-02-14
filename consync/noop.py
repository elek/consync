import requests
import logging

class Noop:
    def __init__(self):
        pass

    def write(self, resource):
        logging.info("Emulated write to " + resource.path)
        for source in resource.sources:
            logging.info("  source: " + source)

    def list(self):
        return[]


    def close(self):
        pass