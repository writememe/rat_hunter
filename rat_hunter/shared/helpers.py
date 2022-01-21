from datetime import datetime
from dateutil import tz
from typing import Any

# Import shared settings
from rat_hunter.shared.settings import (
    LOCAL_TZ,
    TIMESTAMP,
    LOGGER,
)  # noqa (import not at top)


def add_google_map_address_url(row: Any) -> str:
    """
    Functions to categorise all types of payments
    by assessing each row using a string match.

    :param row: The pandas row to be categories
    """
    google_maps_url = f"https://maps.google.com/maps?q={row['lat']},{row['lng']}"
    # google_maps_url = google_maps_url.replace(" ", "%20%")
    return google_maps_url


def add_price_in_dollars(row: Any) -> float:
    """
    Functions to categorise all types of payments
    by assessing each row using a string match.

    :param row: The pandas row to be categories
    """
    dollars = float(row["priceInCents"] / 100)
    return dollars


def convert_date_to_local_time(row: Any) -> datetime:
    # Assign UTC time to a variable
    from_zone = tz.tzutc()
    # Auto-detect local machine time
    to_zone = LOCAL_TZ
    parsed_date = row["date"]
    # Example string:
    # 2022-01-13T02:09:35.458Z
    utc = datetime.strptime(parsed_date, "%Y-%m-%dT%H:%M:%S.%fZ")
    utc = utc.replace(tzinfo=from_zone)
    local_date = utc.astimezone(to_zone)
    return local_date


def convert_updated_at_to_local_time(row: Any) -> datetime:
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
    return local_update_at


def convert_created_at_to_local_time(row: Any) -> datetime:
    # Assign UTC time to a variable
    from_zone = tz.tzutc()
    # Auto-detect local machine time
    to_zone = LOCAL_TZ
    parsed_date = row["createdAt"]
    # Example string:
    # 2022-01-13T02:09:35.458Z
    utc = datetime.strptime(parsed_date, "%Y-%m-%dT%H:%M:%S.%fZ")
    utc = utc.replace(tzinfo=from_zone)
    local_created_at = utc.astimezone(to_zone)
    return local_created_at


def calculate_diff_in_minutes(
    other_time: Any,
    timestamp: Any = TIMESTAMP,
) -> int:
    time_delta = timestamp - other_time
    total_seconds = time_delta.total_seconds()
    minutes = round(number=(total_seconds / 60))
    return minutes


def convert_updated_at_to_mins_ago(row: Any) -> int:
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
    # diff_in_mins = calculate_diff_in_minutes(other_time=local_update_at)
    LOGGER.debug(f"Diff in mins: {minutes}")
    # diff_mins_string = f"{diff_in_mins} minutes ago"
    return minutes
