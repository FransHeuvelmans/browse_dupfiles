"""Command line interface"""
import argparse
import sys
from browse_dejadup import loader
from browse_dejadup import tree


def promptbrowse(tree):
    """A simple prompt with faux commands to browse the filetree"""
    tree_pref = tree
    while True:
        rd = input("-->: ")
        rd_lst = rd.split(" ", 1)

        # Change a dir
        if rd_lst[0] == "cd":
            if len(rd_lst) < 2:
                print("Need a directory name")
                continue
            if rd_lst[1] == "..":
                if tree_pref.parent != None:
                    print("Moving up")
                    tree_pref = tree_pref.parent
                else:
                    print("Top level")
                continue
            changed = False
            for nd in tree_pref.contents:
                if nd.name == rd_lst[1]:
                    print("Changing to dir ", rd_lst[1])
                    tree_pref = nd
                    changed = True
                    break
            if not changed:
                print("Node not found ", rd_lst[1])
        # list files
        elif rd == "ls":
            print([l.name for l in tree_pref.contents])
        elif rd == "name":
            print(tree_pref)
        # quit
        elif rd == "q":
            print("Quitting")
            break
        else:
            print("Unknown command: ", rd)


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Browse large duplicity logfiles")
    parser.add_argument(
        "logfile", metavar="N", type=str, help="an integer for the accumulator"
    )

    args = parser.parse_args()
    num, tree = loader.load_file(args.logfile)
    print(num)
    promptbrowse(tree)
