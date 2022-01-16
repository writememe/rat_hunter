"""
Example usage of rat_hunter to search for all Victorian
places with RATs in stock and send an email to a distribution
list using yagmail (Gmail)
"""
import os
import sys

# Get path of the current dir under which the file is executed
dirname = os.path.dirname(os.path.abspath(__file__))
# Assign the root project directory to a variable
BASE_CODE_DIR = os.path.abspath(os.path.join(dirname, "..", ".."))
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
    TIMESTAMP,
    LOCAL_TZ_NAME,
)  # noqa (import not at top)

"""
Example code block after imports
"""
# Instantiate a live copy of the findarat data
find_a_rat_data = RATResults(online=True)
# Specify your address query (effectively does a partial match, case-insentive)
"""
Other examples
address_query = "3226"
address_query = "Australia"
address_query = "Geelong"

In addition to this, it takes regex queries as well:
address_query = "VIC\s3\d\d\d"  # noqa
address_query = "(3939|3064)"
address_query = "322[0-9]"
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
gipps_address_query = f"({'|'.join(gippsland_postcodes)})"
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
geelong_address_query = f"({'|'.join(geelong_area_postcodes)})"
darebin_area_postcodes = [
    "3070",
    "3071",
    "3072",
    "3073",
    "3078",
]
darebin_address_query = f"({'|'.join(darebin_area_postcodes)})"


# Apply the filter and return the results as a Pandas dataframe
gipps_data = find_a_rat_data.filter_by_address(
    address=gipps_address_query, in_stock=True
)
file_name = "gippsland_rat_results.csv"
file_path = os.path.join(RESULT_DIR, file_name)
# Save the results offline to a CSV file
vic_data_df = export_to_csv(df=gipps_data, file_name=file_name, output_dir=RESULT_DIR)
# Compile the metadata needed for the email notification (all dynamic)
metadata = {
    "last_run": TIMESTAMP,
    "search_query": gipps_address_query,
    "timezone": LOCAL_TZ_NAME,
}
# Setup your recipients to recieve the email as a list
gippsland_cc_address_list = ["danielfjteycheney@gmail.com"]
# Send it!
dispatch_html_email(
    df_file_path=file_path, cc_address_list=gippsland_cc_address_list, kwargs=metadata
)
geel_data = find_a_rat_data.filter_by_address(
    address=geelong_address_query, in_stock=True
)
file_name = "greater_geelong_rat_results.csv"
file_path = os.path.join(RESULT_DIR, file_name)
# Save the results offline to a CSV file
geel_data_df = export_to_csv(df=geel_data, file_name=file_name, output_dir=RESULT_DIR)
# Compile the metadata needed for the email notification (all dynamic)
metadata = {
    "last_run": TIMESTAMP,
    "search_query": geelong_address_query,
    "timezone": LOCAL_TZ_NAME,
}
# Setup your recipients to recieve the email as a list
geel_cc_address_list = ["danielfjteycheney@gmail.com"]
# Send it!
dispatch_html_email(
    df_file_path=file_path, cc_address_list=geel_cc_address_list, kwargs=metadata
)

darebin_data = find_a_rat_data.filter_by_address(
    address=darebin_address_query, in_stock=True
)
file_name = "darebin_rat_results.csv"
file_path = os.path.join(RESULT_DIR, file_name)
# Save the results offline to a CSV file
geel_data_df = export_to_csv(
    df=darebin_data, file_name=file_name, output_dir=RESULT_DIR
)
# Compile the metadata needed for the email notification (all dynamic)
metadata = {
    "last_run": TIMESTAMP,
    "search_query": darebin_address_query,
    "timezone": LOCAL_TZ_NAME,
}
# Setup your recipients to receive the email as a list
darebin_cc_address_list = ["danielfjteycheney@gmail.com"]
# Send it!
dispatch_html_email(
    df_file_path=file_path, cc_address_list=darebin_cc_address_list, kwargs=metadata
)
