# taskmanager/tasks.py

from celery import shared_task
from .coinmarketcap_scraper import CoinMarketCapScraper

@shared_task
def scrape_coin_data(coin):
    scraper = CoinMarketCapScraper(coin)
    return scraper.get_coin_data()
