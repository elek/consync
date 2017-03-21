#!/usr/bin/env python
import argparse
import logging
import os

from consync.adapter_env import EnvAdapter
from watchdog.events import FileSystemEventHandler
import time
from consync.noop import Noop
from consync.reader import Reader
from consync.compose import Compose
from consync.template import Template
from consync.transform import Transform
from consync.flag import Flag
from consync.profiles import Profiles
from consync.adapter_consul import ConsulAdapter
from consync.adapter_file import FileAdapter
from watchdog.observers import Observer
import configparser

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class MyEventHandler(FileSystemEventHandler):
    def __init__(self, sync, resources):
        self.sync = sync
        self.resources = resources

    def on_modified(self, event):
        if not event.is_directory:
            print(event.event_type)
            print(event.src_path)

            modified_resources = [resource for resource in self.resources if event.src_path in resource.sources]
            self.sync.process(self.resources, modified_resources)


class ConSync:
    def __init__(self, args):
        self.args = args
        self.basepath = args.dir
        if self.args.file:
            self.adapter = FileAdapter(self.args.file)
        elif self.args.env:
            self.adapter = EnvAdapter(self.args.env)
        else:
            self.adapter = ConsulAdapter(self.args.url, self.args.prefix)

        config = configparser.ConfigParser()
        config_file = os.path.join(args.dir, 'consync.ini')
        if os.path.exists(config_file):
            config.read(config_file)

        config['common'] = {'basepath': self.basepath}

        profiles = ""
        if self.args.profiles:
            profiles += self.args.profiles
        if config['profiles'].get("active",''):
            profiles += config['profiles']['active']
        config['profiles'] = {'active': profiles}

        self.plugins = []
        self.plugins.append(Reader(config))
        self.plugins.append(Flag(config))
        self.plugins.append(Compose(config))
        self.plugins.append(Profiles(config))
        self.plugins.append(Template(config))
        if not self.args.env:
            self.plugins.append(Transform(config))

    def run(self):
        if self.args.serve:
            adapter = self.adapter
            # detect dependencies
            self.adapter = Noop()
            resources = self.collect()
            self.process(resources, resources)

            self.adapter = adapter
            self.clean(resources)
            event_handler = MyEventHandler(self, resources)
            observer = Observer()
            observer.schedule(event_handler, self.args.dir, recursive=True)
            observer.start()
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                observer.stop()
            observer.join()


        else:
            resources = self.collect()
            self.clean(resources)
            self.process(resources, resources)

    def clean(self, resources):
        resources_pathes = [resource.path for resource in resources]
        for path in self.adapter.list():
            if path not in resources_pathes:
                self.adapter.remove(path)

    def collect(self):
        resources = []
        for plugin in self.plugins:
            plugin.collect_resources(resources)
        logger.info(resources)
        return resources

    def process(self, all_resources, resources):
        for resource in all_resources:
            resource.content = b''
            for plugin in self.plugins:
                plugin.read(resource)
        for plugin in self.plugins:
            for resource in all_resources:
                plugin.transform_content(all_resources, resource)
        for resource in resources:
            self.adapter.write(resource)
        self.adapter.close()

def main():
   parser = argparse.ArgumentParser()
   parser.add_argument("dir", help="directory to upload")
   parser.add_argument("prefix", help="prefix path in consul kv")
   parser.add_argument("--serve", help="Listening for new changes and upload only the changed files", action="store_true")
   parser.add_argument("--url", help="consul server address (protocol, servername, port)")
   parser.add_argument("--file", help="Generate config files to the specified directory instead of upload to the consul")
   parser.add_argument("--env", help="Print out prefixed variables as environment variables")
   parser.add_argument("--profiles", help="Comma separated list of the activated profiles")
   args = parser.parse_args()
   c = ConSync(args)
   c.run()

if __name__ == "__main__":
    main()