
class Resource:
    def __init__(self, path):
        self.content = ""
        self.path = path
        self.sources = []

    def __repr__(self):
        return self.path