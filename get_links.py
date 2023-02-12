from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from config import Config as cfg
from time import sleep
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import requests
import openpyxl
import json
from seleniumwire.utils import decode
import json
from utils import scrape_reqs_for_graphs
from typing import List


class UrlsScrapper:
    def __init__(self, file_path):
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(options=chrome_options)
        self.driver = driver
        self.offset = 0
        self.file_path = file_path
        self.login()
        self.curr_urls = self.get_saved_urls()
        self.set_page(1)

    def set_page(self, page):
        self.driver.get(f"https://steamcommunity.com/market/search?appid=753#p{page}_popular_desc")

    def login(self):
        self.driver.get('https://steamcommunity.com/login/home/?goto=profiles%2F76561198462126877%2F')
        login_field = self._look_for_ele(By.XPATH, '/html/body/div[1]/div[7]/div[4]/div[1]/div[1]/div/div/div/div[2]/div/form/div[1]/input')
        login_field.send_keys(cfg.LOGIN)
        pass_field = self._look_for_ele(By.XPATH, '/html/body/div[1]/div[7]/div[4]/div[1]/div[1]/div/div/div/div[2]/div/form/div[2]/input')
        pass_field.send_keys(cfg.PASSWORD)
        login_btn = self._look_for_ele(By.XPATH, '/html/body/div[1]/div[7]/div[4]/div[1]/div[1]/div/div/div/div[2]/div/form/div[4]/button')
        login_btn.click()
        eq_btn = self._look_for_ele(By.XPATH, '/html/body/div[1]/div[7]/div[6]/div[1]/div[3]/div/div[1]/div[2]/div[3]/div[2]/a/span[1]')

    def _look_for_ele(self, by, value):
        ele = None
        try:
            ele = self.driver.find_element(by, value)
        except Exception:
            sleep(0.2)
            ele = self._look_for_ele(by, value)
        return ele

    def get_saved_urls(self) -> set:
        with open(self.file_path, 'r') as f:
            data = json.load(f)
            urls_arr = data['links']
        return set(urls_arr)

    def save_urls(self, urls: List[str]):
        with open(self.file_path, 'r') as f:
            data = json.load(f)
            data['links'].extend(urls)

        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=4)

    def is_new_url(self, url) -> bool:
        res = url not in self.curr_urls
        print(res)
        return url not in self.curr_urls

    def add_url_to_current_urls(self, url):
        self.curr_urls.add(url)

    def get_curr_page_urls(self) -> List[str]:
        urls_eles = self.driver.find_elements(By.CLASS_NAME, 'market_listing_row_link')
        urls_arr = []
        for ele in urls_eles:
            try:
                href = ele.get_attribute('href')
                urls_arr.append(href)
            except Exception:
                pass
        return urls_arr


def main():
    app = UrlsScrapper('links.json')
    page = 1
    while True:
        on_page_urls = app.get_curr_page_urls()
        new_urls = list(filter(lambda url: app.is_new_url(url), on_page_urls))
        for url in new_urls:
            app.add_url_to_current_urls(url)
        app.save_urls(new_urls)
        page += 1
        sleep(1)
        app.set_page(page)


if __name__ == '__main__':
    main()
