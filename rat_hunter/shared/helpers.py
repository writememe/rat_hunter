"""
This module contains a series of helper functions which are consumed in other
areas of the application
"""
# Import modules
from datetime import datetime
from dateutil import tz
from typing import Any

from pandas import DataFrame

# Import shared settings
from rat_hunter.shared.settings import (
    LOCAL_TZ,
    TIMESTAMP,
    LOGGER,
)  # noqa (import not at top)


def add_google_map_address_url(row: Any) -> str:
    """
    Formulate a Google Maps URL based on the longitude and latitude from the Pandas row.

    Args:
        row: The pandas row to be analysed
    Raises:
        N/A
    Returns:
        google_maps_url: A Google Maps URL which will take you to the RAT location using
        the longitude and latitude from the Pandas row.
    """
    return f"https://maps.google.com/maps?q={row['lat']},{row['lng']}"


def add_price_in_dollars(row: Any) -> float:
    """
    Calculate the price in dollars by converting the value of the 'priceInCents` to dollars.

    Args:
        row: The pandas row to be analysed
    Raises:
        N/A
    Returns:
        dollars: The price in dollars, calculated from the price in cents.
    """
    return float(row["priceInCents"] / 100)


def convert_date_to_local_time(row: Any) -> datetime:
    """
    Convert the 'date' field from UTC time to the application's local time.

    Args:
        row: The pandas row to be analysed
    Raises:
        N/A
    Returns:
        local_date: The date converted into the local time.
    """
    # Assign UTC time to a variable
    from_zone = tz.tzutc()
    # Auto-detect local machine time
    to_zone = LOCAL_TZ
    parsed_date = row["date"]
    # Example string:
    # 2022-01-13T02:09:35.458Z
    utc = datetime.strptime(parsed_date, "%Y-%m-%dT%H:%M:%S.%fZ")
    utc = utc.replace(tzinfo=from_zone)
    return utc.astimezone(to_zone)


def convert_updated_at_to_local_time(row: Any) -> datetime:
    """
    Convert the 'updatedAt' field from UTC time to the application's local time.

    Args:
        row: The pandas row to be analysed
    Raises:
        N/A
    Returns:
        local_update_at: The date converted into the local time.
    """
    # Assign UTC time to a variable
    from_zone = tz.tzutc()
    # Auto-detect local machine time
    to_zone = LOCAL_TZ
    parsed_date = row["updatedAt"]
    # Example string:
    # 2022-01-13T02:09:35.458Z
    utc = datetime.strptime(parsed_date, "%Y-%m-%dT%H:%M:%S.%fZ")
    utc = utc.replace(tzinfo=from_zone)
    return utc.astimezone(to_zone)


def convert_created_at_to_local_time(row: Any) -> datetime:
    """
    Convert the 'createdAt' field from UTC time to the application's local time.

    Args:
        row: The pandas row to be analysed.
    Raises:
        N/A
    Returns:
        local_created_at: The date converted into the local time.
    """
    # Assign UTC time to a variable
    from_zone = tz.tzutc()
    # Auto-detect local machine time
    to_zone = LOCAL_TZ
    parsed_date = row["createdAt"]
    # Example string:
    # 2022-01-13T02:09:35.458Z
    utc = datetime.strptime(parsed_date, "%Y-%m-%dT%H:%M:%S.%fZ")
    utc = utc.replace(tzinfo=from_zone)
    return utc.astimezone(to_zone)


def calculate_diff_in_minutes(
    other_time: Any,
    timestamp: Any = TIMESTAMP,
) -> int:
    """
    Calculate the difference in minutes between two timestamps.

    Args:
        other_time: The time which you want to calculate the difference from.
        timestamp: A timestamp of when the application was initialised.
    Raises:
        N/A
    Returns:
        minutes: The numbers of minutes difference.
    """
    time_delta = timestamp - other_time
    total_seconds = time_delta.total_seconds()
    return round(number=(total_seconds / 60))


def convert_updated_at_to_mins_ago(row: Any) -> int:
    """
    Calculate how long ago this entry was last updated, compared to the timestamp
    of when this application was run.

    Args:
        row: The pandas row to be analysed.
    Raises:
        N/A
    Returns:
        minutes: The numbers of minutes ago that this entry was updated.
    """
    # Assign UTC time to a variable
    from_zone = tz.tzutc()
    # Auto-detect local machine time
    to_zone = LOCAL_TZ
    parsed_date = row["updatedAt"]
    # Example string:
    # 2022-01-13T02:09:35.458Z
    utc = datetime.strptime(parsed_date, "%Y-%m-%dT%H:%M:%S.%fZ")
    utc = utc.replace(tzinfo=from_zone)
    local_update_at = utc.astimezone(to_zone)
    time_delta = TIMESTAMP - local_update_at
    total_seconds = time_delta.total_seconds()
    minutes = round(number=(total_seconds / 60))
    LOGGER.debug(f"Diff in mins: {minutes}")
    return minutes


def filter_aged_entries(
    df: DataFrame, column_name: str = "last_updated_mins_ago", minutes: int = 180
) -> DataFrame:
    """
    Filter a dataframe to remove "aged" entries which are considered too old to be a reliable
    result.

    Args:
        df: The Pandas dataframe to be modified.
        column_name: The column name to filter on.
        minutes: A integer value of entries to keep between 0 and that number.
            Example: 180 would keep all entries that are between 0 and 180 minutes old.
    Raises:
        N/A
    Returns:
        df: The Pandas dataframe after it has been modified.
    """
    original_entry_count = len(df.index)
    df = df[(df[column_name] <= minutes)]
    final_entry_count = len(df.index)
    removed_entries = original_entry_count - final_entry_count
    LOGGER.info(
        f"{removed_entries} entries removed, {final_entry_count} have been retained."
    )
    return df
