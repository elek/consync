import os
from os import path

from consync.resource import Resource


class Profiles:
    def __init__(self, config):
        self.config = config
        self.basepath = config['common']['basepath']
        self.profilesdir = config['common'].get("profilesdir", os.path.join(self.basepath, "profiles"))
        self.profiles = []
        if 'profiles' in config:
           self.profiles = [profile.strip() for profile in config['profiles']['active'].split(",") if profile.strip()]
        print("active profiles: " + " ".join(self.profiles))

    def read(self, resource):
        for profile in self.profiles:
            filepath = path.join(self.profilesdir, profile, resource.path)
            if path.exists(filepath):
                with open(filepath, "rb") as f:
                    if len(resource.content) > 0:
                        resource.content += b'\n'
                    resource.content += f.read()

    def collect_resources(self, resources):
        existing_pathes = [res.path for res in resources]
        for profile in self.profiles:
            profiledir = os.path.join(self.profilesdir, profile)
            for root, dirs, files in os.walk(profiledir, topdown=True):
                dirs[:] = [d for d in dirs if not d.startswith(".")]
                for file in files:
                    filepath = os.path.join(root, file)
                    key = os.path.relpath(filepath, profiledir)
                    if not key in existing_pathes:
                        resource = Resource(os.path.relpath(filepath, profiledir))
                        resource.sources.append(filepath)
                        resources.append(resource)
                    else:
                        resource = [resource for resource in resources if resource.path == key][0]
                        resource.sources.append(filepath)
        return resources

    def filter_resources(self, resources):
        return resources

    def transform_content(self, resources, resource):
        pass
