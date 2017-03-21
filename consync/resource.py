
class Resource:
    def __init__(self, path):
        self.content = b''
        self.path = path
        self.sources = []
        self.flag = 0

    def __repr__(self):
        return self.path