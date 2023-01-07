from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from config import Config as cfg
from time import sleep


class App:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(options=chrome_options)

        self.driver = driver

    def login(self):
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


def main():
    app = App()
    app.login()
    app.driver.get('https://steamcommunity.com/market/listings/753/1245620-Caravan')
    item_id = app.driver.execute_script("return ItemActivityTicker.m_llItemNameID")
    print(item_id)

if __name__ == '__main__':
    main()
