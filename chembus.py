# chembus.py — v3.0
# Global chemical router and matcher for modular brain chemistry

class ChemBus:
    def __init__(self):
        self.chema = []
        self.sources = []

    def register_source(self, func):
        self.sources.append(func)

    def tick(self):
        for source in self.sources:
            new_chema = source()
            if new_chema:
                self.chema.extend(new_chema)

    def extract_matching(self, chrec):
        matching = [c for c in self.chema if chrec(c)]
        self.chema = [c for c in self.chema if not chrec(c)]
        return matching

    def get_all(self):
        return list(self.chema)
