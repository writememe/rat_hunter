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
from rat_hunter.ingestors.base.base import RATResults

# Import the Gmail sender functions
from rat_hunter.exporters.gmail import dispatch_html_email

# Import to CSV exporter function
from rat_hunter.exporters.files import export_to_csv

# Import some shared settings (optional)
from rat_hunter.shared.settings import RESULT_DIR, TIMESTAMP, LOCAL_TZ_NAME

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
"""
address_query = "VIC"
# Apply the filter and return the results as a Pandas dataframe
vic_data = find_a_rat_data.filter_by_address(address=address_query)
file_name = "vic_rat_results.csv"
file_path = os.path.join(RESULT_DIR, file_name)
# Save the results offline to a CSV file
vic_data_df = export_to_csv(df=vic_data, file_name=file_name, output_dir=RESULT_DIR)
# Compile the metadata needed for the email notification (all dynamic)
metadata = {
    "last_run": TIMESTAMP,
    "search_query": address_query,
    "timezone": LOCAL_TZ_NAME,
}
# Setup your recipients to recieve the email as a list
to_address_list = ["ratreceivers@gmail.com"]
# Send it!
dispatch_html_email(
    df_file_path=file_path, to_address_list=to_address_list, kwargs=metadata
)
