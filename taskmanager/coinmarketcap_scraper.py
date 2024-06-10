# taskmanager/coinmarketcap_scraper.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

class CoinMarketCapScraper:
    BASE_URL = 'https://coinmarketcap.com/currencies/'

    def __init__(self, coin):
        self.coin = coin.lower()

    def get_coin_data(self):
        url = f"{self.BASE_URL}{self.coin}/"
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        driver.get(url)

  

        data = {}
        try:
            # Update these XPaths with the correct ones found during inspection
            data['price'] = driver.find_element(By.XPATH, "//span[@class='sc-d1ede7e3-0 fsQm base-text']").text
            data['price_change'] = driver.find_element(By.CSS_SELECTOR, "div[class='sc-d1ede7e3-0 kzFEmO'] p[class='sc-71024e3e-0 sc-58c82cf9-1 bgxfSG iPawMI']").text
            data['market_cap'] = driver.find_element(By.XPATH, "//div[@class='sc-d1ede7e3-0 bwRagp']//div[1]//div[1]//dd[1]").text
            data['market_cap_rank'] = driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(3) > section:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > dl:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > span:nth-child(2)").text
            data['volume'] = driver.find_element(By.XPATH,  "//body[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div[2]/section[2]/div[1]/div[1]/div[1]/dl[1]/div[2]/div[1]/dd[1]").text
            data['volume_rank'] = driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(3) > section:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > dl:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > span:nth-child(2)").text
            data['volume_change'] = driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(3) > section:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > dl:nth-child(2) > div:nth-child(3) > div:nth-child(1) > dd:nth-child(2)").text
            data['circulating_supply'] = driver.find_element(By.CSS_SELECTOR,  "body > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(3) > section:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > dl:nth-child(2) > div:nth-child(4) > div:nth-child(1) > dd:nth-child(2)").text
            data['total_supply'] = driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(3) > section:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > dl:nth-child(2) > div:nth-child(5) > div:nth-child(1) > dd:nth-child(2)").text
            data['diluted_market_cap'] = driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(3) > section:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > dl:nth-child(2) > div:nth-child(7) > div:nth-child(1) > dd:nth-child(2)").text

            # Contracts
            data['contracts'] = []
            contract_elements = driver.find_elements(By.XPATH, "//body[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div[2]/section[2]/div[1]/div[2]/div[1]/div[2]/div[1]")
            for element in contract_elements:
                name = element.find_element(By.XPATH, "//span[contains(@class,'sc-71024e3e-0 dEZnuB')]").text
                address = element.find_element(By.XPATH, "//span[contains(@class,'sc-71024e3e-0 eESYbg address')]").text
                data['contracts'].append({'name': name, 'address': address})

            # Official Links
            data['official_links'] = []
            link_elements = driver.find_elements(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(3) > section:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2)")
            for element in link_elements:
                name = element.find_element(By.CSS_SELECTOR, "a[rel='nofollow noopener'][href='https://dukocoin.com/']").text
               
                data['official_links'].append({'name': name})

            # Socials
            data['socials'] = []
            social_elements = driver.find_elements(By.XPATH, "//body/div[@id='__next']/div[@class='sc-8fab8d8d-1 kYUKSZ global-layout-v2']/div[@class='main-content']/div[@class='cmc-body-wrapper']/div[@class='grid full-width-layout']/div[@class='sc-4c05d6ef-0 sc-305b596a-0 dlQYLv bJydpq']/div[@class='sc-4c05d6ef-0 sc-55349342-0 dlQYLv gELPTu coin-stats']/div[@class='sc-d1ede7e3-0 jLnhLV']/section[@data-hydration-on-demand='true']/div[@class='sc-d1ede7e3-0 jkmmuA content_folded']/div[@class='sc-d1ede7e3-0 cvkYMS coin-info-links']/div[2]")
            for element in social_elements:
                name1 = element.find_element(By.XPATH, "//body[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div[2]/section[2]/div[1]/div[2]/div[3]/div[2]/div[1]/div[1]").text
                name2 = element.find_element(By.XPATH, "//a[@rel='nofollow noopener'][normalize-space()='Telegram']").text

                data['socials'].append({'name1': name1,'name2':name2 })

        except Exception as e:
            data['error'] = str(e)
        finally:
            driver.quit()

        return data
