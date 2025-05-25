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
        "-w", "--words",
        action="store_true",
        help="Print the word counts"
    )
    parser.add_argument(
        "-m", "--chars",
        action="store_true",
        help="Print the character counts"
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
            line_count_val = None
            word_count_val = None
            char_count_val = None
            byte_count_val = None

            # Determine if we are in default mode (no flags specified)
            is_default_mode = not (args.lines or args.words or args.bytes or args.chars)

            # Calculate all requested values first
            if args.lines or is_default_mode:
                try:
                    with open(args.filename, 'r') as f:
                        line_count_val = sum(1 for _ in f)
                except Exception as e:
                    print(f"wc: Could not read {args.filename} for line count: {e}", file=sys.stderr)
            
            if args.words or is_default_mode:
                try:
                    with open(args.filename, 'r') as f:
                        content = f.read()
                        word_count_val = len(content.split())
                except Exception as e:
                    print(f"wc: Could not read {args.filename} for word count: {e}", file=sys.stderr)

            if args.chars:
                try:
                    with open(args.filename, 'r') as f:
                        content = f.read()
                        char_count_val = len(content)
                except Exception as e:
                    print(f"wc: Could not read {args.filename} for char count: {e}", file=sys.stderr)

            if args.bytes or (is_default_mode and not args.chars):
                try:
                    byte_count_val = os.path.getsize(args.filename)
                except Exception as e: 
                    print(f"wc: Could not get size of {args.filename}: {e}", file=sys.stderr)
            
            # Construct output string based on flags or default mode
            if is_default_mode:
                if line_count_val is not None:
                    output_to_print.append(str(line_count_val))
                if word_count_val is not None:
                    output_to_print.append(str(word_count_val))
                if byte_count_val is not None:
                     output_to_print.append(str(byte_count_val))
            else:
                if args.lines and line_count_val is not None:
                    output_to_print.append(str(line_count_val))
                if args.words and word_count_val is not None:
                    output_to_print.append(str(word_count_val))
                if args.chars and char_count_val is not None:
                    output_to_print.append(str(char_count_val))
                if args.bytes and byte_count_val is not None:
                    output_to_print.append(str(byte_count_val))

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
    elif args.words:
        print("Reading from stdin for word count is not yet implemented if -w is specified without a file.", file=sys.stderr)
    elif args.chars:
        print("Reading from stdin for char count is not yet implemented if -m is specified without a file.", file=sys.stderr)
    elif args.bytes:
        print("Reading from stdin for byte count is not yet implemented if -c is specified without a file.", file=sys.stderr)


if __name__ == "__main__":
    main() 