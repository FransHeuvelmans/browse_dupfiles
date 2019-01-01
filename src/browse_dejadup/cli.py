"""Command line interface"""
import sys
import argparse
import curses
from browse_dejadup import loader
from browse_dejadup.tree import Node


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
            if str(nd) == dirnm:
                if type(nd) == Node:
                    print("Changing to dir ", dirnm)
                    tree_pref = nd
                    return
                else:
                    print(dirnm, " is not a directory")
                    return
            elif dirnm == str(nd)[: len(dirnm)]:
                pos_dirs.append(nd)
        if len(pos_dirs) > 1:
            print("Possible dirs: ", [str(l) for l in pos_dirs])
            return
        if pos_dirs:
            if type(pos_dirs[0]) == Node:
                print("Changing to dir ", pos_dirs[0])
                tree_pref = pos_dirs[0]
                return
            else:
                print("Possible loc ", pos_dirs[0], " is not a dir")
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
            print([str(l) for l in tree_pref.contents])
        elif rd == "ll":
            for l in tree_pref.contents:
                print(l)
        elif rd == "name":
            print(tree_pref)
        elif rd == "pwd":
            loc = tree_pref
            full_str = str(loc)
            while loc.parent:
                loc = loc.parent
                full_str = str(loc) + "/" + full_str
            print(full_str)
        # quit
        elif rd == "q":
            print("Quitting")
            break
        elif (rd == "h") or (rd == "help"):
            print("List of commands:")
            print("cd .. | dirname : Change directory up or down")
            print("ls              : List of files/dirs in current dir")
            print("ll              : List of files/dirs underneath")
            print("name            : Name of current file/dir")
            print("pwd             : Current path")
            print("q               : Quit")
        else:
            print("Unknown command: ", rd, " -- press 'h' for help")


def cursesbrowse(stdscr, tree):
    """A Ncurses style browser for exploring the filetree"""
    tree_pref = tree

    # Info for drawing the interface
    contents_loc = [0, 0]  # Option selected
    windows_loc = 0  # window moved from original position
    viewinfo = [[], []]  # 2 lists with all the str info

    def draw_obj(y, c, side, num, printlen):
        """Helper function to draw a single object"""
        if num >= len(viewinfo[side]):
            return  # Can't print
        if contents_loc == [num, side]:
            stdscr.addstr(y, c, viewinfo[side][num][:printlen], curses.A_STANDOUT)
        else:
            stdscr.addstr(y, c, viewinfo[side][num][:printlen])

    def draw_frame():
        """Draw the data's viewinfo model"""
        # curses sets some global vars when initialized so disable pylint
        # pylint: disable=no-member
        curses.update_lines_cols()
        curses.curs_set(0)
        stdscr.clear()
        half_point = int(curses.COLS / 2)
        stdscr.vline(0, half_point, "|", curses.LINES - 2)

        l1_len = min(curses.LINES - 2, len(viewinfo[0]))
        for line in range(l1_len):
            draw_obj(line, 0, 0, line + windows_loc, half_point)

        l2_len = min(curses.LINES - 2, len(viewinfo[1]))
        for line in range(l2_len):
            max_linesize = curses.COLS - half_point - 1
            draw_obj(line, half_point + 1, 1, line + windows_loc, max_linesize)

        # Put 2 or 3 simple info tips in the lowest position
        stdscr.hline(curses.LINES - 2, 0, "-", curses.COLS - 1)
        stdscr.addstr(
            curses.LINES - 1,
            0,
            "q for quit -- arrows to move -- enter to enter"[: curses.COLS - 1],
        )

        stdscr.refresh()

    def process_enter():
        """Enter button pressed need to move tree reference"""
        nonlocal tree_pref

        if tree_pref.parent:
            # Assume there is a '.'
            if contents_loc == [0, 0]:
                tree_pref = tree_pref.parent
                return
            else:
                lst_loc = contents_loc[0] + (contents_loc[1] * len(viewinfo[0])) - 1
        else:
            lst_loc = contents_loc[0] + (contents_loc[1] * len(viewinfo[0]))
        if type(tree_pref.contents[lst_loc]) == Node:
            tree_pref = tree_pref.contents[lst_loc]

    def process_input():
        """Process keyboard input from user"""
        # pylint: disable=no-member
        nonlocal contents_loc, windows_loc
        key = stdscr.getch()
        if key == ord("q"):
            return True
        if key == ord("b"):
            # Go back (or go to the first option)
            contents_loc = [0, 0]
            windows_loc = 0
            process_enter()
        elif key == curses.KEY_UP:
            if contents_loc[0] > 0:
                if contents_loc[0] == windows_loc:
                    windows_loc -= 1
                contents_loc[0] -= 1
        elif key == curses.KEY_DOWN:
            if contents_loc[0] < (len(viewinfo[contents_loc[1]]) - 1):
                if contents_loc[0] == (curses.LINES - 3 + windows_loc):
                    windows_loc += 1
                contents_loc[0] += 1
        elif key == curses.KEY_LEFT:
            if (contents_loc[1] == 1) and (len(viewinfo[0]) > contents_loc[0]):
                contents_loc[1] = 0
        elif key == curses.KEY_RIGHT:
            if (contents_loc[1] == 0) and (len(viewinfo[1]) > contents_loc[0]):
                contents_loc[1] = 1
        elif key == curses.KEY_ENTER or key == 10 or key == 13:
            process_enter()
            contents_loc = [0, 0]
            windows_loc = 0
        return False

    def fill_viewinfo():
        """Update the ''model'' of the data (viewdata)"""
        nonlocal viewinfo
        left = []
        if tree_pref.parent:
            left.append(".")
        total_child_nodes = len(tree_pref.contents)
        if total_child_nodes == 0:
            viewinfo = [left, []]
            return
        elif total_child_nodes == 1:
            left.append(str(tree_pref.contents[0]))
            viewinfo = [left, []]
            return
        else:
            half = total_child_nodes // 2
            name_list = [str(nod) for nod in tree_pref.contents]
            left += name_list[:half]
            right = name_list[half:]
            viewinfo = [left, right]

    while True:
        fill_viewinfo()
        draw_frame()
        stop = process_input()
        if stop:
            break


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Browse large duplicity logfiles")
    parser.add_argument(
        "--prmpt", action="store_true", help="browse using a command prompt"
    )
    parser.add_argument(
        "logfile", type=str, help="duplicity list-current-files outputfile"
    )

    args = parser.parse_args()
    num, tree = loader.load_file(args.logfile)
    print(num)
    if args.prmpt:
        promptbrowse(tree)
    else:
        curses.wrapper(cursesbrowse, tree)

