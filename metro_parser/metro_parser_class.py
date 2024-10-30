import asyncio
import copy
import json
import os
from typing import Any

from aiohttp import ClientSession

from metro_parser.config import (
    ROOT_DIR,
    MetroURLs,
    base_logger,
)


l = base_logger(__name__)


class MetroParser:
    """
    MetroParser is responsible for collecting and processing product data from Metro trade centers.

    This class provides methods to asynchronously fetch product data from specified trade centers
    and store the collected data in a structured format. It utilizes `aiohttp` for making HTTP requests
    and processes the data to extract relevant product information.
    """

    def __init__(self) -> None:
        """
        Initializes a new instance of the MetroParser class.

        This constructor sets up the initial state of the MetroParser instance,
        including initializing the `collected_data` attribute as an empty list
        to store product data collected from trade centers.
        """

        self.collected_data: dict[str, list[dict[str, int | str | None]]] = {}

    async def _fetch_products_for_tradecenter(
        self, session: ClientSession, tradecenter_id: int, query: dict[str, Any]
    ) -> None:
        """
        Asynchronously fetches product data for a specific trade center.

        This method sends a GraphQL query to the Metro API to retrieve information about products
        in the specified trade center. The fetched data is processed and stored in the
        `collected_data` attribute of the class instance.

        :param session: An active aiohttp session for making HTTP requests.
        :param tradecenter_id: Identifier of the trade center.
        :param query: GraphQL query for fetching product data.
        """

        query["variables"]["storeId"] = tradecenter_id
        l.debug(f"Fetching products for tradecenter {tradecenter_id}")
        async with await session.post(
            MetroURLs.METRO_GRAPHQL_URL.value,
            json=query,
        ) as all_products_in_store_response:
            if all_products_in_store_response.status == 200:
                self.collected_data[f"tradecenter {tradecenter_id}"] = [
                    {
                        "id": product["id"],
                        "name": product["name"],
                        "url": f"https://online.metro-cc.ru{product["url"]}",
                        "regular_price": (
                            product["stocks"][0]["prices"]["price"]
                            if product["stocks"][0]["prices"]["old_price"] is None
                            else product["stocks"][0]["prices"]["old_price"]
                        ),
                        "promotional_price": (
                            product["stocks"][0]["prices"]["old_price"]
                            if product["stocks"][0]["prices"]["old_price"] is None
                            else product["stocks"][0]["prices"]["price"]
                        ),
                        "brand": product["manufacturer"]["name"],
                    }
                    for product in (await all_products_in_store_response.json())["data"]["category"]["products"]
                ]
                l.debug(
                    f"{len(self.collected_data[f'tradecenter {tradecenter_id}'])} products fetched "
                    f"for tradecenter {tradecenter_id}"
                )
            else:
                l.error(
                    f"Error while trying to fetch products for tradecenter {tradecenter_id}:\n"
                    f"{MetroURLs.METRO_GRAPHQL_URL.value}\n"
                    "query:\n"
                    f"{query}\n\n"
                    f"{all_products_in_store_response.status}\n"
                    f"{await all_products_in_store_response.text()}"
                )
                return

    async def collect_data(self) -> None:
        """
        Asynchronously collects product data from specified trade centers.

        This method sends HTTP requests to the Metro API to fetch product data from trade centers
        located in Moscow and Saint Petersburg. The fetched data is processed and stored in the
        `collected_data` attribute of the class instance.

        The method uses the aiohttp library for asynchronous HTTP requests and asyncio for managing
        the asynchronous tasks. It fetches the list of all trade centers, filters the trade centers based
        on their city, and then fetches product data for each filtered trade center concurrently using
        asyncio's gather function.

        The fetched product data is stored in the `collected_data` attribute as a dictionary, where
        the keys are the trade center identifiers and the values are lists of dictionaries containing
        product information. Each product dictionary contains the following keys:
        - id: Identifier of the product.
        - name: Name of the product.
        - url: URL of the product on the Metro website.
        - regular_price: Regular price of the product.
        - promotional_price: Promotional price of the product.
        - brand: Brand of the product.

        Note: This method does not return any value. The collected data is stored in the `collected_data` attribute
        of the class instance.
        """

        async with ClientSession() as session:
            cities = ("Москва", "Санкт-Петербург")
            l.debug("Fetching all trade centers")
            async with await session.get(MetroURLs.ALL_TRADECENTERS_URL.value) as all_tradecenters_response:
                if all_tradecenters_response.status == 200:
                    filtered_tradecenter_ids: tuple[int, ...] = tuple(
                        tradecenter["store_id"]
                        for tradecenter in (await all_tradecenters_response.json())["data"]
                        if tradecenter["city"] in cities
                    )
                    l.debug(
                        f"Fetched {len(filtered_tradecenter_ids)} trade centers in {cities}: {filtered_tradecenter_ids}"
                    )
                else:
                    l.error(
                        "Error while trying to fetch all trade centers:\n"
                        f"{MetroURLs.ALL_TRADECENTERS_URL.value}\n"
                        f"{all_tradecenters_response.status}\n"
                        f"{await all_tradecenters_response.text()}"
                    )
                    return

            all_products_in_store_query = copy.deepcopy(
                MetroURLs.MetroGraphQLConstants.value.ALL_PRODUCTS_IN_STORE_QUERY.value  # type: ignore[attr-defined]
            )
            await asyncio.gather(
                *(
                    self._fetch_products_for_tradecenter(session, tradecenter_id, all_products_in_store_query)
                    for tradecenter_id in filtered_tradecenter_ids
                )
            )

    async def dump_data(self) -> None:
        """
        Saves the collected product data to a JSON file.

        This method writes the data stored in the `collected_data` attribute of the class instance
        to a JSON file named "collected_data.json" located in the `"data/"` directory. The JSON file
        is formatted with indentation for better readability.
        """

        data_dir = os.path.join(ROOT_DIR, "data")
        os.makedirs(data_dir, exist_ok=True)
        l.debug(f"Dumping collected products data to JSON file in data directory {data_dir}")
        with open(os.path.join(data_dir, "collected_data.json"), "w", encoding="utf-8") as file:
            json.dump(self.collected_data, file, ensure_ascii=False, indent=4)
