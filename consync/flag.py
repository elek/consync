import os
import re

class Flag:
    def __init__(self, config):
        self.config = config
        self.confdir = os.path.join(self.config['common']['basepath'], "configuration")

    def collect_resources(self, resources):
        return resources

    def read(self, resource):
        pass

    def filter_resources(self, resources):
        return resources

    def transform_content(self, resources, resource):
        for key in self.config['flags']:
            parts = key.split("_")
            pattern = self.config['flags'][key]
            if re.match(pattern, resource.path):
                resource.flag += int(parts[1])
        pass