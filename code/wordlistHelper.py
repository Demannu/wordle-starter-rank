class WordlistHelper:
    def __init__(self):
        self.words = set()

    def combine(self, other):
        for item in other:
            self.words.add(item)

    def load(self, path):
        with open(path) as file:
            for line in file.readlines():
                self.words.add(line)

    def count(self):
        return len(self.words)
