import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import chromedriver_autoinstaller


class FreeNanoFaucetBot:
    def __init__(self, faucet, wallets):
        chromedriver_autoinstaller.install()
        self.driver = webdriver.Chrome(chrome_options=self.setup_chrome_options())
        self.faucet = faucet
        self.wallets = wallets

    def setup_chrome_options(self):
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_prefs = {}
        chrome_options.experimental_options["prefs"] = chrome_prefs
        chrome_prefs["profile.default_content_settings"] = {"images": 2}
        return chrome_options

    def teardown(self):
        self.driver.close()

    def run(self):
        self.driver.get(self.faucet.url)
        self.driver.find_element(By.ID, "nanoAddr") \
            .send_keys(self.wallets.data[0]['address'])
        self.driver.find_element(By.ID, "getNano").click()

        p_element = WebDriverWait(self.driver, 10) \
            .until(lambda x: x.find_element_by_xpath('//*[@id="body-body-wrap"]/div/p/strong'))
        print(f'server response: {p_element.text}')
