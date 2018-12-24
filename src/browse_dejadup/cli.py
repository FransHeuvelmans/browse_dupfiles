"""Command line interface"""
import argparse
import sys
from browse_dejadup import loader


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Browse large duplicity logfiles")
    parser.add_argument(
        "logfile", metavar="N", type=str, help="an integer for the accumulator"
    )

    args = parser.parse_args()
    num, tree = loader.load_file(args.logfile)
    #tree.uprint()
    print(num)
