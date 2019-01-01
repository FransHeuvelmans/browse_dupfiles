"""Loads a log file into a dict structure"""
import logging
import sys
from browse_dejadup.tree import Node


def process_line(log_line):
    """Process a single full log string"""
    splt = log_line.split(maxsplit=5)
    folder_list = splt[-1].split("/")
    return [f.strip() for f in folder_list]


def load_file(file_name):
    """Load a file"""
    total = 0
    log_tree = None

    def process_fldrs(fldrs):
        nonlocal log_tree
        if (len(fldrs) == 1) and (fldrs[0] == "."):
            return
        if log_tree is None:
            log_tree = Node(fldrs[0])
        log_tree.add_children(fldrs)

    with open(file_name) as bigf:
        started = False

        for line in bigf:
            if started:
                fldrs = process_line(line)
                total += 1
                if total % 1234 == 0:
                    print(total, end="\r")
                process_fldrs(fldrs)
            else:
                if "Last full backup date" in line:
                    started = True
    return total, log_tree
