"""
Example usage of rat_hunter to search for various postcodes
with RATs in stock and save the output to a CSV file
"""
import os
import sys

# Get path of the current dir under which the file is executed
dirname = os.path.dirname(os.path.abspath(__file__))
# Assign the root project directory to a variable
BASE_CODE_DIR = os.path.abspath(
    os.path.join(
        dirname,
        "..",
    )
)
sys.path.append(BASE_CODE_DIR)

# Import the RatResult Class
from rat_hunter.ingestors.base.base import RATResults  # noqa (import not at top)

# Import the Gmail sender functions
from rat_hunter.exporters.gmail import dispatch_html_email  # noqa (import not at top)

# Import to CSV exporter function
from rat_hunter.exporters.files import export_to_csv  # noqa (import not at top)

# Import some shared settings (optional)
from rat_hunter.shared.settings import (
    RESULT_DIR,
)  # noqa (import not at top)

# Instantiate a live copy of the findarat data
find_a_rat_data = RATResults(online=True)
# Specify a list of postcodes that you want to query, in this example, its Greater Geelong
# postcodes
postcodes = [
    "3212",
    "3214",
    "3215",
    "3216",
    "3217",
    "3218",
    "3219",
    "3220",
    "3221",
    "3222",
    "3223",
    "3224",
    "3225",
    "3226",
    "3227",
    "3340",
]
postcode_address_query = f"({'|'.join(postcodes)})"
# Apply the filter and return the results as a Pandas dataframe
postcode_data = find_a_rat_data.filter_by_address(
    address=postcode_address_query, in_stock=True
)
# Compile the name and path to the file
file_name = "exported_rat_results.csv"
file_path = os.path.join(RESULT_DIR, file_name)
# Save the results offline to a CSV file
export_to_csv(df=postcode_data, file_name=file_name, output_dir=RESULT_DIR)
