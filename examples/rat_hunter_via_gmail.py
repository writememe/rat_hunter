"""
Example usage of rat_hunter to search for various postcodes
with RATs in stock and send an email to a distribution
list using yagmail (Gmail)
"""
import os
import sys
from typing import List

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
# from rat_hunter.ingestors.base.base import RATResults  # noqa (import not at top)
from rat_hunter.ingestors.au.findarat.findarat import (
    FindARATResults,
)  # noqa (import not at top)

# Import the Gmail sender functions
from rat_hunter.exporters.gmail import dispatch_html_email  # noqa (import not at top)

# Import to CSV exporter function
from rat_hunter.exporters.files import export_to_csv  # noqa (import not at top)

# Import some shared settings (optional)
from rat_hunter.shared.settings import (
    RESULT_DIR,
    TIMESTAMP,
    LOCAL_TZ_NAME,
)  # noqa (import not at top)


def send_postcode_based_alert(
    postcodes: List[str] = ["3000", "3001"],
    common_search_name: str = "melbourne_area",
    cc_address_list: List[str] = ["rathunterworldwide@gmail.com"],
    empty_notification: bool = False,
) -> None:
    """
    Example workflow function which performs the following:

    - Instantiate a live copy of the RAT result data
    - Filter the RAT result data by a list of postcodes
    - Save the results to a CSV, for offline usage
    - If eligible matches are found, send a formatted email via Gmail
    to the CC address list

    Args:
        postcodes: A list of postcodes to be searched against.
        common_search_name: The common search name, used to prefix to the outputted CSV file.
        cc_address_list: A list of recipients for the email to be CCed to
        empty_notification: Send an email notification, even when there are no eligible results.
    Returns:
        N/A
    Raises:
        N/A

    """
    # Instantiate a live copy of the findarat data
    # find_a_rat_data = RATResults(online=True)
    find_a_rat_data = FindARATResults(online=True)
    # Join the list of postcodes into a viable regex string
    # For example: 3000|3001
    postcode_address_query = f"{'|'.join(postcodes)}"
    # Apply the filter and return the results as a Pandas dataframe
    postcode_data = find_a_rat_data.filter_by_address(
        address=postcode_address_query, in_stock=True
    )
    file_name = f"{common_search_name}_rat_results.csv"
    file_path = os.path.join(RESULT_DIR, file_name)
    # Save the results offline to a CSV file
    export_to_csv(df=postcode_data, file_name=file_name, output_dir=RESULT_DIR)
    # Compile the metadata needed for the email notification (all dynamic)
    metadata = {
        "last_run": TIMESTAMP,
        "search_query": postcode_address_query,
        "timezone": LOCAL_TZ_NAME,
    }
    # Send it!
    dispatch_html_email(
        df_file_path=file_path,
        cc_address_list=cc_address_list,
        kwargs=metadata,
        empty_notification=empty_notification,
    )


"""
Specify some list of postcodes and common names for those postcodes. They will be used
later on to call the example workflow function.
"""
gippsland_postcodes = [
    "3950",
    "3951",
    "3953",
    "3954",
    "3956",
    "3959",
    "3960",
    "3981",
    "3991",
    "3995",
    "3996",
]
geelong_area_postcodes = [
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
darebin_area_postcodes = [
    "3070",
    "3071",
    "3072",
    "3073",
    "3078",
]
whittlesea_melbourne_area_postcodes = [
    "3070",
    "3071",
    "3072",
    "3073",
    "3074",
    "3075",
    "3076",
    "3205",
    "3206",
    "3000",
]
"""
Call the example workflow function and specify a common name
for the outputted CSV file
"""
send_postcode_based_alert(
    postcodes=darebin_area_postcodes,
    common_search_name="darebin",
    cc_address_list=["rathunterworldwide@gmail.com"],
)
send_postcode_based_alert(
    postcodes=gippsland_postcodes,
    common_search_name="gippsland",
    cc_address_list=["rathunterworldwide@gmail.com"],
    empty_notification=True,
)
send_postcode_based_alert(
    postcodes=gippsland_postcodes,
    common_search_name="geelong",
    cc_address_list=["rathunterworldwide@gmail.com"],
)
send_postcode_based_alert(
    postcodes=whittlesea_melbourne_area_postcodes,
    common_search_name="whittlesea_melbourne",
    cc_address_list=["rathunterworldwide@gmail.com"],
)
