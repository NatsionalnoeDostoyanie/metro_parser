import logging
from enum import Enum
from pathlib import Path


class MetroURLs(Enum):
    """
    The MetroURLs class is an enumeration that contains various URLs related to the Metro project.

    This class provides a centralized location for managing and accessing these URLs,
    making it easier to maintain and update them.
    """

    class MetroGraphQLConstants(Enum):
        """
        The MetroGraphQLConstants class is an enumeration that contains various constants related to GraphQL queries.

        This class provides a centralized location for managing and accessing these constants,
        making it easier to maintain and update them.
        """

        _GQL_MAX_INT = 2_147_483_647

        # Use with `MetroURLs.METRO_GRAPHQL_URL` for POST-requests, define the "storeId"
        ALL_PRODUCTS_IN_STORE_QUERY = {
            "query": """
                query Category($storeId: Int!, $slug: String!, $inStock: Boolean, $from: Int!, $size: Int!) {
                    category(storeId: $storeId, slug: $slug, inStock: $inStock) {
                        products(from: $from, size: $size) {
                            id
                            name
                            url
                            stocks {
                                prices {
                                    price
                                    old_price
                                }
                            }
                            manufacturer {
                                name
                            }
                        }
                    }
                }
            """,
            "variables": {
                "storeId": None,
                "slug": "kofe",
                "inStock": True,
                "from": 0,
                "size": _GQL_MAX_INT,
            },
        }

    ALL_TRADECENTERS_URL = "https://api.metro-cc.ru/api/v1/tradecenters/"

    METRO_GRAPHQL_URL = "https://api.metro-cc.ru/products-api/graph"


def base_logger(module_name: str | None = None) -> logging.Logger:
    """
    Creates a logger instance setting up basic config and using the given `module_name` as the logger name.

    If no `module_name` is specified, the logger name will be `"root"`.

    :param module_name: Name of the module to use as logger name.

    :returns: The logger instance with the specified module name and basic config.
    """

    logging.basicConfig(
        level=logging.DEBUG, format="%(levelname)s - %(asctime)s - %(name)s - %(funcName)s:%(lineno)d - %(message)s"
    )
    return logging.getLogger(module_name)


ROOT_DIR = Path(__file__).parent.parent
