import path_setup
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
from utils import scrape_reqs_for_graphs, load_urls, get_sell_price
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, ElementClickInterceptedException


class SellApp:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://steamcommunity.com/login/home/?goto=profiles%2F76561198462126877")

        self.driver = driver
        self.offset = 0

    def login(self):
        login_field = self._look_for_ele(By.XPATH, '/html/body/div[1]/div[7]/div[4]/div[1]/div[1]/div/div/div/div[2]/div/form/div[1]/input')
        login_field.send_keys(cfg.LOGIN)
        pass_field = self._look_for_ele(By.XPATH, '/html/body/div[1]/div[7]/div[4]/div[1]/div[1]/div/div/div/div[2]/div/form/div[2]/input')
        pass_field.send_keys(cfg.PASSWORD)
        login_btn = self._look_for_ele(By.XPATH, '/html/body/div[1]/div[7]/div[4]/div[1]/div[1]/div/div/div/div[2]/div/form/div[4]/button')
        login_btn.click()
        eq_btn = self._look_for_ele(By.XPATH, '/html/body/div[1]/div[7]/div[6]/div[1]/div[3]/div/div[1]/div[2]/div[3]/div[2]/a/span[1]')
        self.driver.get('https://steamcommunity.com/profiles/76561198462126877/inventory/#753')

    def _look_for_ele(self, by, value):
        ele = None
        try:
            ele = self.driver.find_element(by, value)
        except Exception:
            sleep(0.2)
            ele = self._look_for_ele(by, value)
        return ele


    def set_correct_window_size(self):
        self.driver.set_window_size(width=900, height=1000)

    def get_all_items(self):
        scrolled_to_bottom = False
        while scrolled_to_bottom is False:
            items = self.driver.find_elements(By.CLASS_NAME, 'itemHolder')
            items_len = len(items)
            self.driver.execute_script('scrollBy(0, 10000)')
            sleep(0.2)
            again_items = self.driver.find_elements(By.CLASS_NAME, 'itemHolder')
            if items_len == len(again_items):
                scrolled_to_bottom = True
        return again_items


    def verify_marketable(self):
        marketable = self.driver.execute_script('return g_ActiveInventory.selectedItem.description.marketable')
        if marketable:
            self.driver.execute_script('SellCurrentSelection()')
        return marketable == 1
        # try:
        #     self.driver.find_element(By.CLASS_NAME, 'item_market_action_button_contents').click()
        #     return True
        # except NoSuchElementException:
        #     self.driver.find_element(By.CLASS_NAME, 'economy_item_popup_dismiss').click()
        #     return False
        # except ElementNotInteractableException:
        #     sleep(0.3)
        #     return self.verify_marketable()

    def close_curr_item(self):
        self.driver.find_element(By.CLASS_NAME, 'economy_item_popup_dismiss').click()

    def get_item_sale_price(self):
        market_hash_name = self.driver.execute_script('return g_ActiveInventory.selectedItem.description.market_hash_name')
        url = f'https://steamcommunity.com/market/listings/753/{market_hash_name}'
        self.driver.execute_script(f"""window.open("{url}")""")
        tabs = self.driver.window_handles
        self.driver.switch_to.window(tabs[1])
        item_id = self.driver.execute_script('return ItemActivityTicker.m_llItemNameID')
        sleep(0.5)
        sell, buy = scrape_reqs_for_graphs(self.driver, item_id)
        return sell, buy

    def scroll_into_clickable_view(self, ele):
        self.driver.execute_script('arguments[0].scrollTo()', ele)
        self.driver.execute_script('scrollBy(0, -200)')

    def sell_item(self, price):
        self.driver.find_element(By.ID, 'market_sell_buyercurrency_input').send_keys(price)

        faq_checked = self.driver.execute_script("return document.getElementById('market_sell_dialog_accept_ssa').checked")
        if not faq_checked:
            self.driver.find_element(By.ID, 'market_sell_dialog_accept_ssa').click()

        self.driver.find_element(By.ID, 'market_sell_dialog_accept').click()
        sleep(0.2)
        self.driver.find_element(By.ID, 'market_sell_dialog_ok').click()

    def click_when_interactable(self, ele):
        try:
            ele.click()
        except ElementClickInterceptedException:
            sleep(0.2)
            self.click_when_interactable(ele)

    def close_remaining_windows(self):
        self.driver.execute_script('g_ActiveItemPopupModal.Dismiss()')
        try:
            sleep(0.3)
            self.driver.find_element(By.XPATH, '/html/body/div[5]/div[3]/div/div[2]/div/span').click()
        except Exception:
            print('exception in dismssing 1')
            sleep(0.2)
            try:
                self.driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/div/div[1]').click()
            except Exception:
                print('exc 2')


def main():
    app = SellApp()
    app.login()
    app.set_correct_window_size()
    items = app.get_all_items()
    print(items)

    for item in items:
        app.scroll_into_clickable_view(item)
        print('scrolled')
        sleep(0.1)
        app.click_when_interactable(item)
        print('clicked')
        # item.click()
        sleep(0.1)
        is_marketable = app.verify_marketable()
        print('verified')
        sleep(0.1)
        if not is_marketable:
            app.close_curr_item()
            continue
        sleep(0.5)
        sell, buy = app.get_item_sale_price()

        tabs = app.driver.window_handles
        app.driver.close()
        app.driver.switch_to.window(tabs[0])
        sleep(0.1)
        sell_price = get_sell_price(sell, 15)
        app.sell_item(sell_price)
        sleep(0.5)

        app.close_remaining_windows()

        print('sell', sell)
        print('buy', buy)


if __name__ == '__main__':
    main()
