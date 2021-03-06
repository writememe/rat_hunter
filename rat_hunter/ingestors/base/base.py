"""
Base class for RAT results.

It's anticipated that this class is sub-classed from the relevant
country folder, should the project continue to grow.
"""
# Import modules
from os import PathLike
import requests
from requests.exceptions import HTTPError
import pandas as pd
from typing import Optional, Dict, Any, Union, List
import os
import sys
import json

from os import path

# Get path of the current directory under which the settings folder is created
dirname = os.path.dirname(__file__)
# Append the repo base directory to the sys path, if it isn't already
repo_base_dir = os.path.join(dirname, "..", "..", "..")
if repo_base_dir not in sys.path:
    sys.path.append(repo_base_dir)
# Import shared settings
from rat_hunter.shared.settings import (
    LOGGER,
    DATA_OUTPUT_DIR,
)  # noqa (import not at top)
from rat_hunter.shared.helpers import (
    add_google_map_address_url,
    add_price_in_dollars,
    convert_date_to_local_time,
    convert_updated_at_to_local_time,
    convert_created_at_to_local_time,
    convert_updated_at_to_mins_ago,
)  # noqa (import not at top)
from rat_hunter.exporters.files import export_to_csv  # noqa (import not at top)


class RATResults(object):
    """
    Base class object for RAT results
    """

    def __init__(
        self,
        url: str = "https://sparkling-voice-bdd0.pipelabs-au.workers.dev/",
        ssl_verify: bool = True,
        online: bool = True,
        offline_data: Optional[List[Dict[Any, Any]]] = None,
        **kwargs: Dict[str, Any],
    ):
        self.url = url
        self.ssl_verify = ssl_verify
        if online:
            self.data = self.ingest_json_payload(url, ssl_verify)
            self.save_json_response(json_data=self.data)
        else:
            LOGGER.warning("Using offline data!")
            self.data = offline_data  # type: ignore

        self.raw_df = self.convert_data_to_df(data=self.data)
        self.df = self.augment_base_data(df=self.raw_df)

    def ingest_json_payload(self, url: str, ssl_verify: bool) -> List[Dict[Any, Any]]:
        """
        Take a URL which contains a JSON payload of RAT data and ingest it into
        a dictionary for further processing.
        Ingest the JSON payload from the RAT URL.

        Args:
            url: The URL which contains the JSON data.
            ssl_verify: Boolean to toggle SSL verification off/on
        Raises:
            N/A
        Returns:
            data: A dictionary of raw RAT data from the JSON payload.
        """
        data: List[Dict[Any, Any]] = [{}]
        try:
            r = requests.get(url=url, verify=ssl_verify)
            r.raise_for_status()
            data = r.json()
            LOGGER.debug(f"Status Code: {r.status_code}")
            LOGGER.debug(f"Response Text: {r.text}")
            LOGGER.debug(f"JSON Payload: {data}")
        except HTTPError as http_err:
            LOGGER.error(f"HTTP Error: {http_err}")
        except Exception as e:
            LOGGER.error(f"Other General Exception Error: {e}")
        return data

    def save_json_response(
        self,
        json_data: List[Dict[Any, Any]],
        file_name: str = "rat_data.json",
        output_dir: Union[str, PathLike] = DATA_OUTPUT_DIR,  # type: ignore
    ) -> None:
        """
        Take a dictionary of data and save it to a JSON file.

        Args:
            json_data: A dictionary of data to be saved to a JSON file.
            file_name: The name of the file to save the data to.
            output_dir: The directory in which the file should be placed.
        Raises:
            N/A
        Returns:
            N/A
        """
        json_file_path = path.abspath(os.path.join(output_dir, file_name))
        with open(json_file_path, "w+") as json_file:
            json.dump(json_data, json_file, indent=2)
        LOGGER.info(f"Data from: {self.url} saved to {json_file.name}")

    def convert_data_to_df(self, data: List[Dict[Any, Any]]) -> pd.DataFrame:
        """
        Convert the data into a Pandas dataframe

        Args:
            data: A dictionary of data to be converted into a Pandas dataframe.
        Raises:
            N/A
        Returns:
            df: The Pandas dataframe created from the original dictionary.
        """
        return pd.DataFrame.from_records(data)  # type:ignore

    def augment_base_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Augment the base RAT data with some additional computed columns:

        - Add the 'google_maps_url' column, computed from an entries longtitude and latitude
        - Add the 'price_in_dollars', computed from the 'priceInCents' column
        - Convert the 'date', 'updatedAt', 'createdAt' from UTC time into the applications local
        timezone and add these columns
        - Add the 'last_updated_mins_ago' column, computed from the 'updatedAt' column

        Args:
            df: The Pandas dataframe to be modified.
        Raises:
            N/A
        Returns:
            df: The Pandas dataframe after it has been augmented.
        """
        df["google_maps_url"] = df.apply(
            lambda row: add_google_map_address_url(row), axis=1
        )
        df["price_in_dollars"] = df.apply(lambda row: add_price_in_dollars(row), axis=1)
        df["date_local_time"] = df.apply(
            lambda row: convert_date_to_local_time(row), axis=1
        )
        df["updatedAt_local_time"] = df.apply(
            lambda row: convert_updated_at_to_local_time(row), axis=1
        )
        df["createdAt_local_time"] = df.apply(
            lambda row: convert_created_at_to_local_time(row),
            axis=1,
        )
        df["last_updated_mins_ago"] = df.apply(
            lambda row: convert_updated_at_to_mins_ago(row),
            axis=1,
        )
        return df

    def filter_by_address(
        self,
        address: str = "",
        in_stock: bool = True,
    ) -> pd.DataFrame:
        """
        Take any regex pattern and filter the address by that criteria, in addition to providing
        'in stock' or 'out of stock' results.

        Args:
            address: The regex pattern which you would like to search for (case-insensitive).
                Examples (in single quotes):
                    -  '3000|3001'
                    - 'Thornbury|Northcote|Preston'
                    - '200[0-9]'
                    - '2\d\d\d'
            in_stock: Boolean to filter results by 'in stock' OR 'out of stock'
        Raises:
            N/A
        Returns:
            df: The Pandas dataframe after it has been filtered.
        """
        raw_df = self.df
        IN_STOCK_STATUSES = ["IN_STOCK", "LOW_STOCK"]
        NO_STOCK_STATUSES = ["NO_STOCK"]
        LOGGER.debug(f"Performing address search for: {address}")
        if in_stock:
            df = raw_df[
                (raw_df["address"].str.contains(pat=address, case=False))
                & (raw_df["status"].isin(IN_STOCK_STATUSES))
            ]
        else:
            df = raw_df[
                (raw_df["address"].str.contains(pat=address, case=False))
                & (raw_df["status"].isin(NO_STOCK_STATUSES))
            ]
        return df


def example_code() -> None:
    """
    Example usage of the class
    """
    # Specify the location to the RAT JSON data
    rat_file_path = os.path.join(
        repo_base_dir, "sample_data", "findarat", "rat_data.json"
    )
    # Load the data into a dictionary
    with open(rat_file_path, "r") as rat_file:
        rat_data = json.load(rat_file)
    # Debug printout
    LOGGER.debug(rat_data)
    # Instantiate the RATResults class, using offline data
    offline_rat = RATResults(online=False, offline_data=rat_data)
    # Filter for Victorian results only
    vic_data = offline_rat.filter_by_address(address="VIC\s3\d\d\d", in_stock=True)
    # Do some printouts
    LOGGER.info(f"First six results for Victoria (3xxx):\n\n{vic_data.head(6)}")
    LOGGER.info(f"Total Victoria (3xxx) Entries: {len(vic_data.index)}")
    # Save results to CSV
    export_to_csv(df=vic_data, file_name="offline_vic_rat.csv")


if __name__ == "__main__":
    example_code()
