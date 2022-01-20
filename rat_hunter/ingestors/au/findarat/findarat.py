"""
Base class for ingesting the backend data to

https://www.findarat.com.au
"""
# Import modules
import os
import sys

# Get path of the current directory under which the settings folder is created
dirname = os.path.dirname(__file__)
# Append the repo base directory to the sys path, if it isn't already
repo_base_dir = os.path.join(dirname, "..", "..", "..", "..")
if repo_base_dir not in sys.path:
    sys.path.append(repo_base_dir)

from rat_hunter.ingestors.base.base import RATResults  # noqa (import not at top)


class FindARATResults(RATResults):
    pass
