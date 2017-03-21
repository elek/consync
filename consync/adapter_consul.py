from urllib.parse import urlparse

import requests
import json
import os
import consul
from consul import Consul


class ConsulAdapter:
    def __init__(self, address, prefix):
        if address[-1] != '/':
            address += '/'
        if address[-6:] != 'v1/kv/':
            address += 'v1/kv/'
        if address[0:4] != "http":
            address = "http://" + address
        if prefix[0] == '/':
            prefix = prefix[1:]
        if prefix[-1] != '/':
            prefix += '/'
        self.prefix = prefix
        self.address = address
        self.address_url = urlparse(self.address)
        self.consul = Consul(self.address_url.hostname, self.address_url.port)

    def write(self, resource):
        url = self.url(resource.path)
        response = self.consul.kv.put(self.prefix + resource.path, resource.content, flags = resource.flag)
        if not response:
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

    def close(self):
        pass
