"""
This module contains a series of exporter file functions
to parse and export Pandas dataframe results.
"""
# Import modules
import os
import sys
from pandas import DataFrame
from os import PathLike
from typing import Any, Union

# Get path of the current directory under which the settings folder is created
dirname = os.path.dirname(__file__)
# Append the repo base directory to the sys path, if it isn't already
repo_base_dir = os.path.join(
    dirname,
    "..",
    "..",
)
if repo_base_dir not in sys.path:
    sys.path.append(repo_base_dir)

from rat_hunter.shared.settings import (
    LOGGER,
    RESULT_DIR,
)  # noqa (import not at top


def export_to_csv(
    df: DataFrame,
    file_name: str = "data.csv",
    output_dir: Union[str, PathLike[Any]] = RESULT_DIR,
):
    """
    Export Pandas dataframe to a CSV file.

    Args:
        df: The pandas dataframe to be exported.
        file_name: The name of the CSV file where the Pandas dataframe will be saved to.
        output_dir: The output directory of the CSV file where the Pandas dataframe will be saved
        to.
    Returns:
        file_path: The fully abstracted path to the CSV file.
    Raises:
        N/A
    """
    file_path = os.path.abspath(os.path.join(output_dir, file_name))
    df.to_csv(file_path, index=False)
    LOGGER.info(f"CSV file saved to: {file_path}")
