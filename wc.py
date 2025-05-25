#!/usr/bin/env python3
import argparse
import os
import sys
import locale 

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
        nargs="?", # 0 or 1 argument, means filename is optional
        help="The file to process. If not specified, reads from stdin."
    )

    args = parser.parse_args()

    line_count_val, word_count_val, char_count_val, byte_count_val = None, None, None, None
    is_default_mode = not (args.lines or args.words or args.bytes or args.chars)
    output_filename_suffix = "" # Will be populated if args.filename exists


    if args.filename:
        output_filename_suffix = f" {args.filename}"
        try:
            file_content_text = None 
            text_ops_needed = args.lines or args.words or args.chars or is_default_mode

            if text_ops_needed:
                with open(args.filename, 'r', encoding='utf-8', errors='replace') as f_text:
                    file_content_text = f_text.read()
            
            if file_content_text is not None:
                if args.lines or is_default_mode:
                    line_count_val = file_content_text.count('\\n')
                if args.words or is_default_mode:
                    word_count_val = len(file_content_text.split())
                if args.chars:
                    char_count_val = len(file_content_text)
            
            if args.bytes or is_default_mode:
                byte_count_val = os.path.getsize(args.filename)

        except FileNotFoundError:
            print(f"wc: {args.filename}: No such file or directory", file=sys.stderr)
            sys.exit(1)
        except Exception as e: 
            print(f"wc: An error occurred processing file {args.filename}: {e}", file=sys.stderr)
            sys.exit(1)

    else: 
        raw_data = sys.stdin.buffer.read() 
        
        if args.bytes or is_default_mode:
            byte_count_val = len(raw_data)

        text_content_needed_for_stdin = args.lines or args.words or args.chars or is_default_mode
        text_content = "" 

        if text_content_needed_for_stdin:
            used_encoding = "utf-8" 
            try:
                stdin_encoding = sys.stdin.encoding
                if stdin_encoding:
                    used_encoding = stdin_encoding
                else:
                    preferred_encoding = locale.getpreferredencoding(False)
                    if preferred_encoding:
                        used_encoding = preferred_encoding
                
                text_content = raw_data.decode(used_encoding, errors='replace')
            except Exception as e:
                print(f"wc: Error decoding stdin using encoding '{used_encoding}': {e}", file=sys.stderr)
            
            if args.lines or is_default_mode:
                line_count_val = text_content.count('\\n')
            if args.words or is_default_mode:
                word_count_val = len(text_content.split())
            if args.chars: 
                char_count_val = len(text_content)

    output_to_print = []
    if is_default_mode:
        if line_count_val is not None: output_to_print.append(str(line_count_val))
        if word_count_val is not None: output_to_print.append(str(word_count_val))
        if byte_count_val is not None: output_to_print.append(str(byte_count_val))
    else:
        if args.lines and line_count_val is not None: output_to_print.append(str(line_count_val))
        if args.words and word_count_val is not None: output_to_print.append(str(word_count_val))
        if args.chars and char_count_val is not None: output_to_print.append(str(char_count_val))
        if args.bytes and byte_count_val is not None: output_to_print.append(str(byte_count_val))

    if output_to_print: 
        print(" ".join(output_to_print) + output_filename_suffix)
    elif not args.filename and is_default_mode:
        print(f"0 0 0{output_filename_suffix}") 

if __name__ == "__main__":
    main() 