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
        elif log_tree is None:
            part = Node(fldrs[-1])
            if len(fldrs) > 1:
                for fldr in fldrs[-2::-1]:
                    old_part = part
                    part = Node(name=fldr, contents=[part])
                    old_part.parent = part
            log_tree = part
        else:
            if fldrs[0] != log_tree.name:
                logging.error("Different base node")
            # TODO: Currently assumes that every fldrs row has the same starting node
            # and that each row thereafter has at least one directory/file below it
            new_base, left_overs = log_tree.get_leaf(fldrs[1:])
            size_left = len(left_overs)
            if size_left < 1:
                logging.warning("Same fldrs line encountered")
                return
            part = Node(left_overs[-1])
            if size_left > 1:
                for lftvr in left_overs[-2::-1]:
                    old_part = part
                    part = Node(name=lftvr, contents=[part])
                    old_part.parent = part
            new_base.contents.append(part)
            part.parent = new_base


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
