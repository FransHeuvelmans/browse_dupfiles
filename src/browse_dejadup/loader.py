"""Loads a log file into a dict structure"""
import logging
from tqdm import tqdm
from .tree import Node


def process_line(log_line):
    """Process a single full log string"""
    splt = log_line.split(sep=" ", maxsplit=5)
    folder_list = splt[-1].split("/")
    return [f.strip() for f in folder_list]


def load_file(file_name):
    """Load a file"""
    total = 0
    log_tree = None


    with open(file_name) as bigf:
        started = False

        for line in tqdm(bigf):
            if started:
                fldrs = process_line(line)
                total += 1
                if (len(fldrs) == 1) and (fldrs[0] == "."):
                    continue
                elif log_tree is None:
                    part = Node(fldrs[-1])
                    if len(fldrs) > 1:
                        for fldr in fldrs[-2::-1]:
                            part = Node(name=fldr, contents=[part])
                    log_tree = part
                else:
                    new_base, left_overs = log_tree.get_leaf(fldrs)
                    size_left = len(left_overs)
                    if size_left < 1:
                        logging.warning("Same fldrs line encountered")
                        continue
                    part = Node(left_overs[-1])
                    if size_left > 1:
                        for lftvr in left_overs[-2::-1]:
                            part = Node(name=lftvr, contents=[part])
                    new_base.contents.append(part)
            else:
                if "Last full backup date" in line:
                    started = True
    return total, log_tree
