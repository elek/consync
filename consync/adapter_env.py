import os
import errno


class EnvAdapter:
    def __init__(self, prefix):
        self.prefix = prefix
        self.values = {}

    def write(self, resource):
        if resource.path.startswith(self.prefix):
            key = resource.path[len(self.prefix) + 1:]
            self.values[key] = resource.content
        pass

    def list(self):
        return []

    def remove(self, key):
        pass

    def close(self):
        for key in self.values.keys():
            ext = self.extension(key)
            if ext and ext == ".xml" or ext == ".properties":
                self.print_file(key, self.values[key])

    def print_file(self, filename, content):
        for line in content.decode("utf-8").split("\n"):
            try:
                sepindex = line.index(":")
                if sepindex > 1:
                    key = line[:sepindex]
                    value = line[sepindex + 1:]
                    print("{}: \"{}\"".format(filename.upper() + "_" + key, value.strip()))
            except ValueError:
                pass

    def extension(self, key):
        index = key.rfind(".")
        if index:
            return key[index:]
        else:
            return None
