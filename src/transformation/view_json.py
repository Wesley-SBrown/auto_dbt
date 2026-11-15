# src/transformation/view_json.py

import json
import argparse

from ..utils import get_output_path

def preview_jsonl(input_file: str, num_lines: int):
    """
    Outputs a preview of the jsonl file

    Parameters
    ----------
    input_file : str
        Input Jsonl file name
    num_lines : int
        Num of json lines to output
    """

    input_path = get_output_path(input_file)

    print(f"Head of jsonl file: {input_file}")

    try:
        with open(input_path, "r", encoding="utf-8") as f:
            for i, line in enumerate(f):
                if i > num_lines:
                    break

                data = json.loads(line.strip())
                print(json.dumps(data, indent=2))

    except json.JSONDecodeError as e:
        print(f"[ERROR] Failed to parse jsonl file: {e}")

if __name__=='__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-l", "--lines", default=2, type=int, 
        help="Number of lines of JSON to display"
    )
    args = parser.parse_args()
    
    preview_jsonl("meta_Automotive.jsonl", args.lines)


