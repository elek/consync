from jinja2 import Environment, FileSystemLoader, StrictUndefined
from jinja2 import TemplateNotFound
from jinja2.loaders import BaseLoader
import os


class ResourceLoader(BaseLoader):
    def __init__(self, resources):
        self.resources = resources
        self.included = []

    def get_source(self, environment, template):
        source = [resource for resource in self.resources if resource.path == template]
        if (len(source)):
            self.included.extend(source[0].sources)
            return (source[0].content,None, lambda: True)
        else:
            raise TemplateNotFound(template)


class Template:
    def __init__(self, basedir):
        self.basedir = basedir

    def read(self, resource):
        pass

    def collect_resources(self, resources):
        pass

    def filter_resources(self, resources):
        return resources

    def transform_content(self, resources, resource):
        loader = ResourceLoader(resources)
        t = Environment(
            loader=loader,
            undefined=StrictUndefined,
            variable_start_string="${",
            variable_end_string="}"
        ).from_string(resource.content)
        resource.content = t.render(os.environ)
        resource.sources.extend([source for source in loader.included if source not in resource.sources])

