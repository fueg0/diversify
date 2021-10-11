class Artist:
    def __init__(self, name, uri, related, graph_level=0):
        self.name = name
        self.uri = uri
        self.related = related
        self.graph_level = graph_level
        self.neighbors = set()

    def start_relationship(self, related):
        self.neighbors.add(related.uri)

        related.neighbors.add(self.uri)
        related.graph_level = 0

    def add_related_neighbor(self, related):
        if related.graph_level <= self.graph_level:
            self.neighbors.add(related.uri)
        else:
            related.neighbors.add(self.uri)
            related.graph_level = (self.graph_level + 1)
