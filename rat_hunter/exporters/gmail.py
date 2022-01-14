"""

"""
# Import modules
from dotenv import load_dotenv
import yagmail
import os
import sys
import pandas as pd
from os import environ
from typing import List, Dict, Any, Optional
from pretty_html_table import build_table

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
    DEFAULT_CRED_ENV,
    LOCAL_TZ_NAME,
)  # noqa (import not at top

"""
Block of code to process the ingestion of environmental
variables
"""
# NOTE: This has been set to always revert to system provided environmental
# variables, rather than what is provided in the .env file using
# the override=False method.
# If nothing is set on the system, the values from the .env file are used.
load_dotenv(dotenv_path=DEFAULT_CRED_ENV, override=True)


# Specify a list of environmental variables
# for usage inside script
environment_variables = [
    "GMAIL_ACC",
    "GMAIL_PWORD",
]
# Iterate over environmental variables and ensure they are set,
# if not exit the program.
for variables in environment_variables:
    if environ.get(variables) is not None:
        LOGGER.info(f"Environmental variable: {variables} is set.")
    else:
        LOGGER.critical(
            f"Environmental variable: {variables} is NOT set, exiting script."
        )
        sys.exit(1)

gmail_acc = environ.get("GMAIL_ACC")
gmail_pword = environ.get("GMAIL_PWORD")


def authorise_yagmail_client(
    gmail_acc: str = gmail_acc, gmail_pword: str = gmail_pword
):
    """
    Instantiate a connection to the yagmail client
    and return for use in other functions.
    Args:
        gmail_acc: The Gmail username used to login to your account.
        gmail_pword: The Gmail password used to login to your account.
    Raises:
        N/A
    Returns:
        yg: An instantiated object, ready for sending emails.
    """
    LOGGER.debug(gmail_acc)
    LOGGER.debug(gmail_pword)
    # print(dir(yagmail))
    yg = yagmail.SMTP(gmail_acc, gmail_pword)
    return yg


def drop_df_columns(
    df,
    drop_columns: List[str] = [
        "createdAt",
        "updatedAt",
        "deletedAt",
        "point",
        "priceInCents",
        "logoPath",
        "link",
        "linkDisplay",
        "polygon",
        "groupID",
        "pricePerN",
        "approved",
        "lat",
        "lng",
    ],
):
    LOGGER.info(f"Dropping '{drop_columns}' from HTML email content")
    df = df.drop(columns=drop_columns)
    return df


def reorder_df_columns(
    df,
    email_columns: List[str] = [
        "name",
        "address",
        "last_updated_mins_ago",
        "price_in_dollars",
        "google_maps_url",
        # "updatedAt_local_time",
        # "createdAt_local_time",
        # "date_local_time",
        "status",
        "verified",
        # "id",
        "date_local_time",
    ],
):
    LOGGER.info(f"Pre Dataframe columns: {df.columns.tolist()}")
    df = df.reindex(columns=email_columns)

    LOGGER.info(f"Post Dataframe columns: {df.columns.tolist()}")
    return df


def trim_and_reorder_df_columns(
    df,
    retained_ordered_columns: List[str] = [
        "name",
        "address",
        "last_updated_mins_ago",
        "price_in_dollars",
        "google_maps_url",
        # "updatedAt_local_time",
        # "createdAt_local_time",
        # "date_local_time",
        "status",
        "verified",
        # "id",
        # "date_local_time",
    ],
) -> pd.DataFrame:
    all_columns = df.columns.tolist()
    remove_columns = list(set(all_columns) - set(retained_ordered_columns))
    LOGGER.info(all_columns)
    LOGGER.info(remove_columns)
    LOGGER.info(retained_ordered_columns)
    # Keep the columns of interest by dropping all other columns
    df = df.drop(columns=remove_columns)
    LOGGER.info(df.head(2))
    # Reorder the columns
    df = df.reindex(columns=retained_ordered_columns)
    df = df.reset_index()
    df = df.drop(columns=["index"])
    LOGGER.info(df.head(2))
    df = df.sort_values(by=["last_updated_mins_ago"])
    return df


def generate_html_base_email_body(**kwargs):
    pass


def parse_results_to_email_content(df, **kwargs: Dict[str, Any]):
    LOGGER.info(f"KWARGS{kwargs}")

    try:
        last_run = kwargs["kwargs"]["kwargs"]["last_run"]
        local_timezone = kwargs["kwargs"]["kwargs"]["timezone"]
        search_query = kwargs["kwargs"]["kwargs"]["search_query"]
    except KeyError as key_err:
        LOGGER.error(
            f"Kwargs not supplied, so email cannot be formatted and sent. Error: {key_err}"
        )
        last_run, local_timezone, search_query = "UNKNOWN", LOCAL_TZ_NAME, "UNKNOWN"
    LOGGER.critical(last_run)
    LOGGER.critical(local_timezone)
    LOGGER.critical(search_query)
    total_entries = len(df.index)
    email_subject = f"RAT Hunter: {total_entries} 🐀 locations found"
    html_df = trim_and_reorder_df_columns(df=df)
    # Build the HTML table using pretty-html-table
    html_table = build_table(
        df=html_df,
        color="green_light",
        font_size="small",
        font_family="Arial, Helvetica, sans-serif",
        text_align="centre",
    )
    html_body = f"""\
    <html>
      <head>RAT hunter has detected <b>{total_entries}</b> locations with RATs using the search query: <b>{search_query}</b>, last updated at: <b>{last_run}</b></head>
      <body>
        <h4><b>All times below are in local timezone</b>: {local_timezone} </h4>
        <br>
        <p>Hello fellow RAT hunter,<br>
           I've found some pesky RATs!:<br>
           {html_table}
           <br>
           Regards,
           <br>
           The RAT hunter 🐀🐀🐀
        </p>
        <h3>This data is automatically parsed from the <a href="https://findarat.com.au/">Find a RAT Website</a></p></h3>
      </body>
    </html>
    """  # noqa
    # """
    # Replace newline characters so that body formats correctly in HTML email
    # https://github.com/kootenpv/yagmail/issues/116
    html_body = html_body.replace("\n", "")
    LOGGER.info(f"HTML BODY: {html_body}")
    return email_subject, html_body


def send_notification(
    to_address_list: Optional[List[str]] = [],
    cc_address_list: Optional[List[str]] = [],
    subject: str = "RATs have been found!",
    body: str = "",
):
    # # Initialise the yagmail client so we can send the email
    yag = authorise_yagmail_client(gmail_acc, gmail_pword)
    # Send the email
    email_result = yag.send(
        to=to_address_list,
        cc=cc_address_list,
        subject=subject,
        contents=[body],
    )
    LOGGER.info(f"Result of email: {email_result}")


def dispatch_html_email(
    df_file_path,
    to_address_list: Optional[List[str]] = [],
    cc_address_list: Optional[List[str]] = [],
    **kwargs,
):
    df = pd.read_csv(df_file_path)
    email_subject, html_body = parse_results_to_email_content(df=df, kwargs=kwargs)
    send_notification(
        to_address_list=to_address_list,
        cc_address_list=cc_address_list,
        subject=email_subject,
        body=html_body,
    )
