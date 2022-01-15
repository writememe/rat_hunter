"""
Base class for ingesting the backend data to

https://www.findarat.com.au
"""
# Import modules
from os import PathLike
import requests
from requests.exceptions import HTTPError
import pandas as pd
from typing import Optional, List, Dict, Any
import os
import sys
import json

# from pydantic import BaseModel
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
        offline_data: Optional[List[Dict[str, Any]]] = None,
        **kwargs,
    ):
        self.url = url
        self.ssl_verify = ssl_verify
        if online:
            self.data = self.ingest_json_payload(url, ssl_verify)
            self.save_json_response(json_data=self.data)
        else:
            LOGGER.warning("Using offline data!")
            self.data = offline_data

        self.raw_df = self.convert_data_to_df(data=self.data)
        self.df = self.augment_base_data(df=self.raw_df)
        # Not needed for now
        # self.df = self.augment_normalised_address_field(df=self.data_df)

    def ingest_json_payload(self, url, ssl_verify):
        """
        Ingest the JSON payload from the RAT URL
        """
        data = {}
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
        json_data,
        file_name: str = "rat_data.json",
        output_dir: PathLike = DATA_OUTPUT_DIR,
    ):
        json_file_path = path.abspath(os.path.join(output_dir, file_name))
        with open(json_file_path, "w+") as json_file:
            json.dump(json_data, json_file, indent=2)
        LOGGER.info(f"Data from: {self.url} saved to {json_file.name}")

    def convert_data_to_df(self, data) -> pd.DataFrame:
        """
        Convert the data (list of dictionaries) into a Pandas dataframe.
        """
        return pd.DataFrame.from_records(data)

    def augment_normalised_address_field(self, df):
        df["address_lower_case"] = df["address"].str.lower()
        LOGGER.info(f"Updated dataframe columns: {df.columns.tolist()}")
        LOGGER.debug(f"Updated dataframe: {df.head(5)}")
        return df

    def augment_base_data(self, df):
        """
        Amend the base data with some additional computed columns
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
    ):
        raw_df = self.df
        IN_STOCK_STATUSES = ["IN_STOCK", "LOW_STOCK"]
        NO_STOCK_STATUSES = ["NO_STOCK"]
        LOGGER.debug(f"Performing address search for: {address}")
        if in_stock:
            df = raw_df[
                (raw_df["address"].str.contains(pat=address, case=False))
                & (raw_df["status"].isin(IN_STOCK_STATUSES))
            ]
            LOGGER.critical(f"filter by address: {df}")
        else:
            df = raw_df[
                (raw_df["address"].str.contains(pat=address, case=False))
                & (raw_df["status"].isin(NO_STOCK_STATUSES))
            ]
            LOGGER.critical(f"filter by address: {df}")
        return df


def example_code():
    rat_file_path = os.path.join(
        repo_base_dir, "sample_data", "findarat", "rat_data.json"
    )

    with open(rat_file_path, "r") as rat_file:
        rat_data = json.load(rat_file)

    LOGGER.debug(rat_data)
    a = RATResults(online=True)
    # LOGGER.debug(a.data)
    # LOGGER.debug((type(a.data)))
    # LOGGER.debug(a.data_df.head(6))
    # LOGGER.info(a.df.head(6))

    act_data = a.filter_by_address(address="VIC", in_stock=True)
    # LOGGER.info(a.df.head(6))
    LOGGER.info(act_data.head(6))
    LOGGER.info(len(act_data.index))

    export_to_csv(df=act_data, file_name="rat.csv")
