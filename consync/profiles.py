import os
from os import path

from consync.resource import Resource


class Profiles:
    def __init__(self, basepath, profiles):
        self.basepath = basepath
        self.profilesdir = os.path.join(basepath, "profiles")
        profile_file = os.path.join(basepath, "profiles.txt")
        self.profiles = []
        if profiles:
            self.profiles.extend(profiles.split(","))
        if os.path.isfile(profile_file):
            with open(profile_file) as f:
                for line in f:
                    line = line.strip()
                    if line:
                        self.profiles.append(line)
        print("active profiles: " + " ".join(self.profiles))

    def read(self, resource):
        for profile in self.profiles:
            filepath = path.join(self.profilesdir, profile, resource.path)
            if path.exists(filepath):
                with open(filepath) as f:
                    resource.content = resource.content + "\n" + f.read()

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
        # keypath = os.path.relpath(filepath, self.basepath)
        # for profile in self.profiles:
        #     extension_file = os.path.join(self.basepath, "profiles", profile, keypath)
        #     if os.path.isfile(extension_file):
        #         with open(extension_file) as f:
        #             print("Using extension file {}".format(extension_file))
        #             content += "\n" + f.read()
        # return content
