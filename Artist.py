class Artist:
    def __init__(self, name, uri, related, graph_level=0):
        self.name = name
        self.uri = uri
        self.related = related
        self.graph_level = graph_level
        self.neighbors = []

    # def __init__(self):
    #     self.name = ''
    #     self.uri = ''
    #     self.related = []
    #     self.graph_level = -1
    #     self.neighbors = []

    def start_relationship(self, related):
        self.neighbors.append(related.uri)

        related.neighbors.append(self.uri)
        related.graph_level = 0

    def add_related_neighbor(self, related):
        if related.graph_level <= self.graph_level:
            self.neighbors.append(related.uri)
        else:
            related.neighbors.append(self.uri)
            related.graph_level = (self.graph_level + 1)
