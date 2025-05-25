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
        "-l", "--lines",
        action="store_true",
        help="Print the newline counts"
    )
    parser.add_argument(
        "filename",
        nargs="?", # 0 or 1 argument, means filename is optional (for stdin later)
        help="The file to process"
    )

    args = parser.parse_args()

    if args.filename:
        try:
            output_to_print = []

            if args.lines:
                try:
                    with open(args.filename, 'r') as f:
                        line_count = sum(1 for _ in f)
                    output_to_print.append(str(line_count))
                except Exception as e:
                    print(f"wc: Could not read {args.filename} for line count: {e}", file=sys.stderr)

            if args.bytes:
                byte_count = os.path.getsize(args.filename)
                output_to_print.append(str(byte_count))
            
            if not args.lines and not args.bytes:
                byte_count = os.path.getsize(args.filename)
                output_to_print.append(str(byte_count))
            
            if output_to_print:
                print(" ".join(output_to_print) + f" {args.filename}")

        except FileNotFoundError:
            print(f"wc: {args.filename}: No such file or directory", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"wc: An error occurred with {args.filename}: {e}", file=sys.stderr)
            sys.exit(1)
    elif args.lines:
        print("Reading from stdin for line count is not yet implemented if -l is specified without a file.", file=sys.stderr)
    elif args.bytes:
        print("Reading from stdin for byte count is not yet implemented if -c is specified without a file.", file=sys.stderr)


if __name__ == "__main__":
    main() 