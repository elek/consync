#!/usr/bin/env python
import argparse
import logging

from watchdog.events import FileSystemEventHandler
import time
from consync.noop import Noop
from consync.reader import Reader
from consync.compose import Compose
from consync.template import Template
from consync.transform import Transform
from consync.profiles import Profiles
from consync.consul import Consul
from consync.file import File
from watchdog.observers import Observer

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
            self.adapter = File(self.args.file)
        else:
            self.adapter = Consul(self.args.url, self.args.prefix)

        self.plugins = []
        self.plugins.append(Reader(self.basepath))
        self.plugins.append(Compose(self.basepath))
        self.plugins.append(Profiles(self.basepath, self.args.profiles))
        self.plugins.append(Template(self.basepath))
        self.plugins.append(Transform(self.basepath))

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
            resource.content = ""
            for plugin in self.plugins:
                plugin.read(resource)
        for plugin in self.plugins:
            for resource in all_resources:
                plugin.transform_content(all_resources, resource)
        for resource in resources:
            self.adapter.write(resource)

def main():
   parser = argparse.ArgumentParser()
   parser.add_argument("dir", help="directory to upload")
   parser.add_argument("prefix", help="prefix path in consul kv")
   parser.add_argument("--serve", help="Listening for new changes and upload only the changed files", action="store_true")
   parser.add_argument("--url", help="consul server address (protocol, servername, port)")
   parser.add_argument("--file", help="Generate config files to the specified directory instead of upload to the consul")
   parser.add_argument("--profiles", help="Comma separated list of the activated profiles")
   args = parser.parse_args()
   c = ConSync(args)
   c.run()

if __name__ == "__main__":
    main()