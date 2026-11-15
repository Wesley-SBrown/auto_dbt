# src/utils.py

from pathlib import Path

def get_output_path(output_filename: str) -> str:
    """
    Get full file path of data file

    Parameters
    ----------
    output_filename: str
        Compressed data file name

    Outputs
    -------
    output_filepath : str
        full file path
    """
    output_filepath = (Path(__file__)
                        .resolve()
                        .parents[2]
                        / "data" / "inputs" / output_filename
                      )
    return output_filepath