import os
import re
from . import transformation

class Transform:

    def __init__(self, config):
        self.config = config
        self.transformations = {}
        self.transformations['xml'] = self.on_text(transformation.to_xml)
        self.transformations['yaml'] = self.on_text(transformation.to_yaml)
        self.transformations['properties'] = self.on_text(transformation.to_properties)
        self.transformations['env'] = self.on_text(transformation.to_env)
        self.transformations['sh'] = self.on_text(transformation.to_sh)


    def read(self, resource):
        pass

    def collect_resources(self, resources):
        return resources

    def on_text(self, text_transform):
        def transform(resources, resource):
            resource.content = text_transform(resource.content.decode("utf-8")).encode("utf-8")

        return transform

    def transform_content(self, resources, resource):
        for format in self.config['format'].keys():
            pattern = self.config['format'][format]
            if re.match(pattern,resource.path):
                if format not in self.transformations:
                    raise AssertionError("No such transformation {}".format(transformation))
                else:
                    self.transformations[format](resources, resource)

