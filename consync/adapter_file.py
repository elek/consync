import os
import errno


class FileAdapter:
    def __init__(self, basedir):
        self.basedir = basedir

    def write(self, resource):
        filename = os.path.join(self.basedir, resource.path)
        self.mkdir_p(os.path.dirname(filename))
        with open(filename, "wb") as file:
            file.write(resource.content)

    def list(self):
        return []

    def remove(self, key):
        pass

    def mkdir_p(self, path):
        try:
            os.makedirs(path)
        except OSError as exc:  # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise

    def close(self):
        pass