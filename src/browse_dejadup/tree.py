class Node:
    """A basic Tree-like structure to store file hierarchy info"""
    def __init__(self, name, contents=None, parent=None):
        if not contents:
            contents = []
        self.name = name
        self.contents = contents
        self.parent = parent

    def __str__(self):
        return str(self.name)

    def get_leaf(self, string_list):
        """Returns the child node with a certain name or itself when not found
        combined with a boolean found"""
        for l in self.contents:
            if l.name == string_list[0]:
                return l.get_leaf(string_list[1:])
        return self, string_list

    def uprint(self, lvl=0):
        """Ugly (depth-first) print"""
        print('-' * lvl, self.name)
        for l in self.contents:
            l.uprint(lvl + 1)
