import argparse
import logging
from datetime import datetime
from bs4 import BeautifulSoup
import requests


logging.basicConfig(encoding='utf-8', level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__file__)


def __init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()

    parser.add_argument('--host',
                        help='The Ingress REST API',
                        default='localhost')

    parser.add_argument('--city',
                        help='City to crawl weather',
                        default='Copenhagen')

    return parser


arg_parser = __init_argparse()
args, _ = arg_parser.parse_known_args()
HOST = args.host
CITY = args.city
logger.info(f"Configuration: {HOST=} {CITY=}")


# Google: 'what is my user agent' and paste into here
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
                         ' AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.3 Safari/605.1.15'}

logger.info(f"User-agent' {headers['User-Agent']}")


def ingest(crawl_time: datetime, name: str, ingest_key: str, ingest_value: str):
    response = requests.post(
        url=f'http://{HOST}:8000/ingest',
        params={
            'crawl_time': crawl_time,
            'pipeline_name': name,
            'ingest_key': ingest_key,
            'ingest_value': ingest_value,
        }
    )
    return response.status_code


def weather_info(city):
    city = city.replace(" ", "+")
    res = requests.get(
        f'https://www.google.com/search?q={city}&hl=en',
        headers=headers)

    soup = BeautifulSoup(res.text, 'html.parser')

    # To find these - use Developer view and check Elements
    location = soup.select('#wob_loc')[0].getText().strip()
    time = soup.select('#wob_dts')[0].getText().strip()
    info = soup.select('#wob_dc')[0].getText().strip()
    weather = soup.select('#wob_tm')[0].getText().strip()

    crawl_time = datetime.utcnow()
    name = 'weather_spider'
    ingest_value = f'"{location}","{time}","{info}","{weather}"'

    response = ingest(crawl_time, name, 'weather-info', ingest_value)
    logger.info(f"Ingested {ingest_value=} @ {crawl_time} with response {response=}")


if __name__ == '__main__':
    weather_info(f"{CITY} Weather")
