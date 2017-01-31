import requests
import json
import os

class Consul:
    def __init__(self, address, prefix):
        if address[-1] != '/':
            address += '/'
        if prefix[0] == '/':
            prefix = prefix[1:]
        if prefix[-1] != '/':
            prefix += '/'
        self.prefix = prefix
        self.address = address

    def write(self, resource):
        url = self.url(resource.path)
        if not requests.put(url, resource.content).ok:
            print("Error on uploading file {} to {}".format(resource.path, url))

    def url(self, keypath):
        return self.address + self.prefix + keypath

    def remove(self, key):
        delete_url = self.url(key)
        if not requests.delete(delete_url).ok:
            print("Key delete was unsuccessfull: %s" % delete_url)

    def list(self):
        result = requests.get(self.address + self.prefix + "?recurse")
        if result.ok:
            entries = json.loads(result.text)
            return [os.path.relpath(entry['Key'],self.prefix) for entry in entries]
        else:
            print("Error on getting existing keys ")
            return []
