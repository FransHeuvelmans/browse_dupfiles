"""Command line interface"""
import argparse
import sys
from browse_dejadup import loader
from browse_dejadup import tree


def promptbrowse(tree):
    """A simple prompt with faux commands to browse the filetree"""
    tree_pref = tree

    def change_dir(dirnm):
        """Change directory"""
        nonlocal tree_pref
        
        # Move on up
        if ".." in dirnm:
            dotlst = dirnm.split("/")
            upcnt = 0
            for dot in dotlst:
                if (dot == "..") and (tree_pref.parent != None):
                    tree_pref = tree_pref.parent
                    upcnt += 1
            if upcnt > 0:
                print("Moving ", "up" * upcnt)
            else:
                print("Top level")
            return

        # Go further down
        pos_dirs = []
        for nd in tree_pref.contents:
            if nd.name == dirnm:
                print("Changing to dir ", dirnm)
                tree_pref = nd
                return
            elif dirnm in nd.name:
                pos_dirs.append(nd)
        if len(pos_dirs) > 1:
            print("Possible dirs: ", [str(l) for l in pos_dirs])
            return
        elif pos_dirs:
            print("Changing to dir ", pos_dirs[0])
            tree_pref = pos_dirs[0]
            return
        print("Node not found ", dirnm)

    while True:
        rd = input("-->: ")
        rd_lst = rd.split(maxsplit=1)

        # Change a dir
        if rd_lst[0] == "cd":
            if len(rd_lst) < 2:
                print("Need a directory name")
                continue
            change_dir(rd_lst[1])
            # Nothing done with all the other dirs mentioned
        # list files
        elif rd == "ls":
            print([l.name for l in tree_pref.contents])
        elif rd == "ll":
            for l in tree_pref.contents:
                print(l)
        elif rd == "name":
            print(tree_pref)
        elif rd == "pwd":
            loc = tree_pref
            full_str = loc.name
            while loc.parent:
                loc = loc.parent
                full_str = loc.name + "/" + full_str
            print(full_str)
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
