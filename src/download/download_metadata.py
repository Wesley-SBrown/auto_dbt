# src/download/download_metadata.py

import gzip
import json
import requests

from ..utils import get_output_path
URL = "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/raw/meta_categories/meta_Automotive.jsonl.gz"


def download_gz(output_file: str) -> None:
    """
    Downloads compressed json automotive parts dataset

    Parameters
    ----------
    output_filename: str
        output file name
    """

    print(f"Downloading to: {output_filename}...")

    output_filepath = get_output_path(output_file)

    try:
        response = requests.get(url=URL, stream=True)
        response.raise_for_status()

        with open(output_filepath, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"Successfully downloaded to: {output_filepath}")

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to download {output_filename}: {e}")

def unzip_gz(zipped_file: str, output_file: str) -> None:
    """
    Unzips downloaded .jsonl.gz file

    Parameters
    ----------
    zipped_file : str
        Compressed json metadata file
    output_file : str
        unzipped file
    """
    zipped_filepath = get_output_path(zipped_file)
    output_filepath = get_output_path(output_file)

    count = 0

    print(f"Unzipping file: {zipped_file}...")

    with gzip.open(zipped_filepath, "rt", encoding="utf-8") as f_in, \
        open(output_filepath, "w", encoding="utf-8") as f_out:
        for line in f_in:
            record = json.loads(line.strip())

            f_out.write(json.dumps(record) + "\n")
            count += 1

    print(f"Unziiped {count} records to: {output_filepath}")


if __name__=='__main__':
    # Download zipped file
    zip_filename = "meta_Automotive.jsonl.gz"
    # download_gz(zip_filename)

    # Extract zipped file
    output_filename = "meta_Automotive.jsonl"
    unzip_gz(zip_filename, output_filename)




