"""
Class for ingesting the backend data from Find A Rat

Front-end website:
https://www.findarat.com.au

Back-end website:
https://sparkling-voice-bdd0.pipelabs-au.workers.dev/

"""
# Import modules
import os
import sys
from typing import Any

# Get path of the current directory under which the settings folder is created
dirname = os.path.dirname(__file__)
# Append the repo base directory to the sys path, if it isn't already
repo_base_dir = os.path.join(dirname, "..", "..", "..", "..")
if repo_base_dir not in sys.path:
    sys.path.append(repo_base_dir)

from rat_hunter.ingestors.base.base import RATResults


class FindARATResults(RATResults):
    """
    A class for interacting with the Find A RAT backend JSON data

    Front-end website:
    https://www.findarat.com.au

    Back-end website:
    https://sparkling-voice-bdd0.pipelabs-au.workers.dev/

    NOTE: This class is a wrapper class for now, so that more specific
    features can be added later on.
    """

    # Initialise class and take variable amount of arguments
    def __init__(self, *vargs: Any, **kwargs: Any) -> None:
        # Inherit RATResults class and take variable amount of arguments
        super().__init__(*vargs, **kwargs)
