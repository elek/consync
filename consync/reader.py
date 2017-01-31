import os
from os import path

from consync.resource import Resource


class Reader:
    def __init__(self, basepath):
        self.basepath = basepath
        self.confdir = os.path.join(self.basepath, "configuration")

    def collect_resources(self, resources):
        for root, dirs, files in os.walk(self.confdir, topdown=True):
            dirs[:] = [d for d in dirs if not d.startswith(".")]
            for file in files:
                filepath = os.path.join(root, file)
                resource = Resource(os.path.relpath(filepath, self.confdir))
                resource.sources.append(filepath)
                resources.append(resource)
        return resources

    def read(self, resource):
        filepath = path.join(self.confdir, resource.path)
        if path.exists(filepath):
            with open(filepath, "rb") as f:
                resource.content = f.read()

    def filter_resources(self, resources):
        return resources

    def transform_content(self, resources, resource):
        pass