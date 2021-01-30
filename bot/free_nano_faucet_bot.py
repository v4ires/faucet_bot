from http_request_randomizer.requests.proxy.requestProxy import RequestProxy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class FreeNanoFaucetBot:
    def __init__(self, faucet, wallets, proxy, with_proxy=False):
        self.driver = webdriver.Chrome(chrome_options=self.setup_chrome_options())
        self.faucet = faucet
        self.wallets = wallets
        self.proxy = proxy
        self.setup_proxy(with_proxy, proxy.countries)

    def setup_chrome_options(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_prefs = {}
        chrome_options.experimental_options["prefs"] = chrome_prefs
        chrome_prefs["profile.default_content_settings"] = {"images": 2}
        return chrome_options

    def setup_proxy(self, with_proxy, countries):
        if with_proxy:
            proxies = RequestProxy().get_proxy_list()
            filtered_proxies = list(filter(lambda x: x.country in countries, proxies))
            current_proxy = filtered_proxies[0].get_address()
            webdriver.DesiredCapabilities.CHROME['proxy'] = {
                "httpProxy": current_proxy,
                "ftpProxy": current_proxy,
                "sslProxy": current_proxy,
                "proxyType": "MANUAL",
            }

    def teardown(self):
        self.driver.close()

    def exec(self):
        self.driver.get(self.faucet.url)
        self.driver.set_window_size(1280, 1001)
        self.driver.find_element(By.ID, "nanoAddr") \
            .send_keys(self.wallets.data[1]['address'])
        self.driver.find_element(By.ID, "getNano").click()

        p_element = WebDriverWait(self.driver, 10) \
            .until(lambda x: x.find_element_by_xpath('//*[@id="body-body-wrap"]/div/p/strong'))
        print(f'server response: {p_element.text}')
        if p_element.text in ["You've received Nano recently, please wait 10 minutes!",
                              "Error. Please try again!"]:
            exit(0)
