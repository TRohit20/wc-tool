#!/usr/bin/env python3
import argparse
import os
import sys

def main():
    parser = argparse.ArgumentParser(description="Word count tool - counts bytes, words, lines.")
    parser.add_argument(
        "-c", "--bytes",
        action="store_true",
        help="Print the byte counts"
    )
    parser.add_argument(
        "filename",
        nargs="?", # 0 or 1 argument, means filename is optional (for stdin later)
        help="The file to process"
    )

    args = parser.parse_args()

    if args.filename:
        try:
            byte_count = os.path.getsize(args.filename)
            if args.bytes:
                print(f"{byte_count} {args.filename}")
            else:
                print(f"{byte_count} {args.filename}")
        except FileNotFoundError:
            print(f"wc: {args.filename}: No such file or directory", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"wc: An error occurred with {args.filename}: {e}", file=sys.stderr)
            sys.exit(1)
    elif args.bytes:
        print("Reading from stdin for byte count is not yet implemented if -c is specified without a file.", file=sys.stderr)


if __name__ == "__main__":
    main() 