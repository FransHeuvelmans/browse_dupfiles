import logging


class Node:
    """A basic Tree-like structure to store file hierarchy info"""

    def __init__(self, name):
        self.name = name
        self.contents = []
        self.parent = None

    def add_children(self, namelist):
        """Add a single child or a list of children"""
        # Check if it starts at this node
        if namelist[0] != self.name:
            logging.warning("Trying to add children to wrong node")
            return
        if len(namelist) < 2:
            return
        new_base, left_overs = self._get_leaf(namelist[1:])
        size_left = len(left_overs)
        if size_left < 1:
            logging.warning("Same fldrs line encountered")
            return
        nleaf = Node(left_overs[-1])
        if size_left > 1:
            for lftvr in left_overs[-2::-1]:
                oleaf = nleaf
                nleaf = Node(name=lftvr)
                nleaf.contents = [oleaf]
                oleaf.parent = nleaf
        new_base.contents.append(nleaf)
        nleaf.parent = new_base

    def __str__(self):
        return str(self.name)

    def _get_leaf(self, string_list):
        """Returns the child node with a certain name or itself when not found
        combined with a boolean found"""
        for l in self.contents:
            if l.name == string_list[0]:
                return l._get_leaf(string_list[1:])
        return self, string_list

    def _uprint(self, lvl=0):
        """Ugly (depth-first) print"""
        print("-" * lvl, self.name)
        for l in self.contents:
            l._uprint(lvl + 1)
