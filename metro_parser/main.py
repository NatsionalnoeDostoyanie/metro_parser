import asyncio

from metro_parser.config import base_logger
from metro_parser.metro_parser_class import MetroParser


l = base_logger(__name__)


async def main() -> None:
    """
    Main function to run the metro parser.

    This function initializes the `MetroParser` object, collects products data using the `collect_data` method,
    and then dumps the collected data using the `dump_data` method.
    """

    metro_parser = MetroParser()

    l.info("Collecting product data")
    await metro_parser.collect_data()

    l.info("Dumping collected products data")
    await metro_parser.dump_data()


if __name__ == "__main__":
    l.info("Starting metro parser")
    asyncio.run(main())
    l.info("Metro parser finished")
