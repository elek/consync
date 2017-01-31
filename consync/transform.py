import os
import re
from . import transformation


class Transform:
    def __init__(self, basepath):
        self.basepath = basepath

    def read(self, resource):
        pass

    def collect_resources(self, resources):
        return resources

    def transform_content(self, resources, resource):
        trans = self.find_transformation(resource.path, self.basepath)
        if trans:
            resource.content = getattr(transformation, "to_%s" % trans)(resource.content)

    def find_transformation(self, filepath, basepath):
        trafofile = os.path.join(basepath, "transformations.txt")
        transfo = ""
        filename = os.path.basename(filepath)
        if os.path.isfile(trafofile):
            with open(trafofile) as f:
                for line in f:
                    line = line.strip()
                    lsep = line.rfind(" ")
                    pattern = line[0:lsep]
                    if re.search(pattern, filename):
                        transfo = line[lsep:].strip()
        if transfo:
            print("Transforming file {} to format {}".format(filepath, transfo))
        return transfo
