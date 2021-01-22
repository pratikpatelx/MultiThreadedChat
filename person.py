class Person:

    def __init__(self, addr, client):
        self.addr = addr
        self.client = client
        self.name = None

    def set_name(self, name):
        self.name = name

    def __repr__(self):
        result = "The client: {0} with IP addr: {1}".format(self.name, self.addr)
        return result
