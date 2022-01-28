"""
This module contains a series of functions for exporting
RAT results via Gmail
"""
# Import modules
from dotenv import load_dotenv
import yagmail
import os
import sys
import pandas as pd
from os import environ
from typing import List, Dict, Any, Optional, Tuple
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
from rat_hunter.shared.helpers import filter_aged_entries

"""
Block of code to process the ingestion of environmental
variables
"""
# NOTE: This has been set to always revert to system provided environmental
# variables, rather than what is provided in the .env file using
# the override=False method.
# If nothing is set on the system, the values from the .env file are used.
load_dotenv(dotenv_path=DEFAULT_CRED_ENV, override=False)


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
        LOGGER.debug(f"Environmental variable: {variables} is set.")
    else:
        LOGGER.critical(
            f"Environmental variable: {variables} is NOT set, exiting script."
        )
        sys.exit(1)
# Assign environmental variables to variables, so that they can be used later on
gmail_acc = environ.get("GMAIL_ACC")
gmail_pword = environ.get("GMAIL_PWORD")


def authorise_yagmail_client(
    gmail_acc: Optional[str] = gmail_acc, gmail_pword: Optional[str] = gmail_pword
) -> yagmail.SMTP:
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
    return yagmail.SMTP(gmail_acc, gmail_pword)


def drop_df_columns(
    df: pd.DataFrame,
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
) -> pd.DataFrame:
    """
    Take a Pandas dataframe and drop (a.k.a remove) those columns from the dataframe
    and return for use in other functions.

    Args:
        df: The Pandas dataframe to be modified.
        drop_columns: List of columns to be dropped.
    Raises:
        N/A
    Returns:
        df: The Pandas dataframe after it has been modified.
    """
    LOGGER.info(f"Dropping '{drop_columns}' from HTML email content")
    df = df.drop(columns=drop_columns)
    return df


def reorder_df_columns(
    df: pd.DataFrame,
    email_columns: List[str] = [
        "name",
        "address",
        "last_updated_mins_ago",
        "price_in_dollars",
        "google_maps_url",
        "status",
        "verified",
        "date_local_time",
    ],
) -> pd.DataFrame:
    """
    Take a Pandas dataframe and reorder the columns in the order specified by the list
    of supplied columns.

    Args:
        df: The Pandas dataframe to be modified.
        email_columns: List of columns in the order that they are desired.
    Raises:
        N/A
    Returns:
        df: The Pandas dataframe after it has been modified.
    """
    LOGGER.debug(f"Pre Dataframe columns: {df.columns.tolist()}")
    df = df.reindex(columns=email_columns)
    LOGGER.debug(f"Post Dataframe columns: {df.columns.tolist()}")
    return df


def trim_and_reorder_df_columns(
    df: pd.DataFrame,
    retained_ordered_columns: List[str] = [
        "name",
        "address",
        "last_updated_mins_ago",
        "price_in_dollars",
        "google_maps_url",
        "status",
        "verified",
        "date_local_time",
    ],
) -> pd.DataFrame:
    """
    Take a Pandas dataframe and perform the following:

    - Remove columns which aren't explicitly defined in the 'retained_ordered_columns' variable
    - Reorder the remaining columns in the exact order defined in the 'retained_ordered_columns'
    variable
    - Drop the index values (not needed for email usage)
    - Sort the dataframe entries by 'last_updated_mins_ago', with newest entries being at the top

    This is used to format the dataframe so it's ready for emailing.

    Args:
        df: The Pandas dataframe to be modified.
        retained_ordered_columns: List of columns to be retained, and in the order that they are
        desired
    Raises:
        N/A
    Returns:
        df: The Pandas dataframe after it has been modified.
    """
    all_columns = df.columns.tolist()
    remove_columns = list(set(all_columns) - set(retained_ordered_columns))
    LOGGER.debug(f"Original set of dataframe columns: {all_columns}")
    LOGGER.debug(f"Columns to be removed: {remove_columns}")
    LOGGER.debug(f"Columns to be retained: {retained_ordered_columns}")
    # Keep the columns of interest by dropping all other columns
    df = df.drop(columns=remove_columns)
    # Reorder the columns
    df = df.reindex(columns=retained_ordered_columns)
    df = df.reset_index()
    df = df.drop(columns=["index"])
    df = df.sort_values(by=["last_updated_mins_ago"])
    return df


def parse_results_to_email_content(
    df: pd.DataFrame, **kwargs: Dict[str, Any]
) -> Tuple[str, str]:
    """
    Take a Pandas dataframe and perform the following:

    - Format the Pandas dataframe, ready to be emailed
    - Add HTML table to the Pandas dataframe
    - Take **kwargs and use those to add some dynamic data to the email
    - Return the HTML body and email subject, ready for sending

    Args:
        df: The Pandas dataframe to be parsed over.
        **kwargs: A dictionary of data which can be used to help formulate the HTML email.
            Example:
                metadata = {
                    "last_run": "2022-01-21 14:05:01.549629+11:00",
                    "search_query": "3000|3001",
                    "timezone": "AEDT ",
                }
    Raises:
        N/A
    Returns:
        email_subject: A dynamically formed subject string which will indicate how many RATs were
        found.
        html_body: A dynamically formed HTML string which will be the body of the email.
    """
    LOGGER.debug(f"**kwargs supplied into email content: {kwargs}")
    try:
        last_run = kwargs["kwargs"]["kwargs"]["last_run"]
        local_timezone = kwargs["kwargs"]["kwargs"]["timezone"]
        search_query = kwargs["kwargs"]["kwargs"]["search_query"]
    except KeyError as key_err:
        LOGGER.error(
            f"Kwargs not supplied, so email cannot be formatted and sent. Error: {key_err}"
        )
        last_run, local_timezone, search_query = "UNKNOWN", LOCAL_TZ_NAME, "UNKNOWN"
    LOGGER.debug(f"Last run parsed metadata: {last_run}")
    LOGGER.debug(f"Local timezone parsed metadata: {local_timezone}")
    LOGGER.debug(f"Search query parsed metadata:{search_query}")
    html_df = trim_and_reorder_df_columns(df=df)
    total_entries = len(html_df.index)
    email_subject = f"RAT Hunter: {total_entries} 🐀 locations found"
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
    # Replace newline characters so that body formats correctly in HTML email
    # https://github.com/kootenpv/yagmail/issues/116
    html_body = html_body.replace("\n", "")
    LOGGER.debug(f"HTML body: {html_body}")
    return email_subject, html_body


def compile_no_results_email(**kwargs: Dict[str, Any]) -> Tuple[str, str]:
    """
    Compile a HTML email when the RAT hunter finds no results (empty dataframe):

    - Take **kwargs and use those to add some dynamic data to the email
    - Return the HTML body and email subject, ready for sending

    Args:
        df: The Pandas dataframe to be parsed over.
        **kwargs: A dictionary of data which can be used to help formulate the HTML email.
            Example:
                metadata = {
                    "last_run": "2022-01-21 14:05:01.549629+11:00",
                    "search_query": "3000|3001",
                    "timezone": "AEDT ",
                }
    Raises:
        N/A
    Returns:
        email_subject: A email subject which indicates that no RATs were found.
        html_body: A dynamically formed HTML string which will be the body of the email.
    """
    try:
        last_run = kwargs["kwargs"]["kwargs"]["last_run"]
        local_timezone = kwargs["kwargs"]["kwargs"]["timezone"]
        search_query = kwargs["kwargs"]["kwargs"]["search_query"]
    except KeyError as key_err:
        LOGGER.error(
            f"Kwargs not supplied, so email cannot be formatted and sent. Error: {key_err}"
        )
        last_run, local_timezone, search_query = "UNKNOWN", LOCAL_TZ_NAME, "UNKNOWN"
    LOGGER.debug(f"Timezone: {local_timezone}")
    email_subject = "RAT Hunter: We're rat out of luck!"
    html_body = f"""\
    <html>
      <head>RAT hunter didn't find any locations with RATs using the search query: <b>{search_query}</b>, last updated at: <b>{last_run}</b></head>
      <body>
        <br>
        <p>Unfortunately, we couldn't find any RATs available in your requested search area. Hopefully we find some next time.<br>
           <br>
           Regards,
           <br>
           The RAT hunter 🐀🐀🐀
        </p>
        <h3>This data is automatically parsed from the <a href="https://findarat.com.au/">Find a RAT Website</a></p></h3>
      </body>
    </html>
    """  # noqa
    # Replace newline characters so that body formats correctly in HTML email
    # https://github.com/kootenpv/yagmail/issues/116
    html_body = html_body.replace("\n", "")
    LOGGER.debug(f"HTML BODY: {html_body}")
    return email_subject, html_body


def send_notification(
    to_address_list: Optional[List[str]] = [],
    cc_address_list: Optional[List[str]] = [],
    subject: str = "RATs have been found!",
    body: str = "",
) -> None:
    """
    Send an email using yagmail to a list of recipients with a body and subject.

    Args:
        to_address_list: A list of emails to send an email to.
            Example:
                ["rathunter@gmail.com", "noreply@rat.org"]
        cc_address_list: A list of emails to cc an email to.
            Example:
                ["rathunter@gmail.com", "noreply@rat.org"]
    Raises:
        N/A
    Returns:
        N/A
    """
    # Initialise the yagmail client so we can send the email
    yag = authorise_yagmail_client(gmail_acc, gmail_pword)
    # Send the email

    if to_address_list:
        LOGGER.info(
            f"Sending email with subject: {subject}. "
            f"'to' recipients: {', '.join(to_address_list)}."
        )
        email_result = yag.send(
            to=to_address_list,
            subject=subject,
            contents=[body],
        )
    elif cc_address_list:
        LOGGER.info(
            f"Sending email with subject: {subject}. "
            f"'cc' recipients: {', '.join(cc_address_list)}."
        )
        email_result = yag.send(
            cc=cc_address_list,
            subject=subject,
            contents=[body],
        )
    else:
        LOGGER.critical("There is no 'to' or 'cc' recipients, cannot send email.")
        return
    if failed_email := bool(email_result):
        LOGGER.error(f"Email unsuccessful. Error: {email_result}")
    else:
        LOGGER.info("Email sent successfully.")


def dispatch_html_email(
    df_file_path: Any,
    to_address_list: Optional[List[str]] = [],
    cc_address_list: Optional[List[str]] = [],
    empty_notification: bool = False,
    minutes: int = 61,
    **kwargs: Dict[str, Any],
) -> None:
    """
    High-level function which performs the following:

    - Reads in a Pandas dataframe from a specified path
    - Based on the Pandas dataframe having data and not having "aged entries",
    it will send a result email
    - Based on the Pandas dataframe having no data or having "aged entries", it can or can not
    send an email.

    Args:
        df_file_path: The path to the Pandas dataframe which you want to process.
        to_address_list: A list of emails to send an email to.
            Example:
                ["rathunter@gmail.com", "noreply@rat.org"]
        cc_address_list: A list of emails to cc an email to.
            Example:
                ["rathunter@gmail.com", "noreply@rat.org"]
        empty_notification: Boolean to toggle sending an email when no results were found in the
        Pandas dataframe.
        minutes: A integer value of entries to keep between 0 and that number.
            Example: 180 would keep all entries that are between 0 and 180 minutes old.
        **kwargs: A dictionary of data which can be used to help formulate the HTML email.
            Example:
                metadata = {
                    "last_run": "2022-01-21 14:05:01.549629+11:00",
                    "search_query": "3000|3001",
                    "timezone": "AEDT ",
                }
    Raises:
        N/A
    Returns:
        N/A
    """
    df = pd.read_csv(df_file_path)
    df = filter_aged_entries(df=df, minutes=minutes)
    if df.empty and empty_notification:
        email_subject, html_body = compile_no_results_email(kwargs=kwargs)
        send_notification(
            to_address_list=to_address_list,
            cc_address_list=cc_address_list,
            subject=email_subject,
            body=html_body,
        )
    elif df.empty:
        LOGGER.warning(
            "RAT results were empty, and sending of email was disabled."
            " No email will be sent."
        )
    else:
        email_subject, html_body = parse_results_to_email_content(df=df, kwargs=kwargs)
        send_notification(
            to_address_list=to_address_list,
            cc_address_list=cc_address_list,
            subject=email_subject,
            body=html_body,
        )
