import requests
import time
import json
import os
from pathlib import Path
from selenium.webdriver.common.proxy import Proxy, ProxyType
import browser_cookie3
from random_word import RandomWords
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.firefox.webdriver import FirefoxProfile
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import WebDriverException, NoSuchElementException, TimeoutException
from random import randrange
from tbselenium.tbdriver import TorBrowserDriver


class AccountGenerator:
    def __init__(self):
        self.reddit_url = "https://www.reddit.com/register/"
        self.pwd = "SuperSecretPassWordDoNotHack01"
        self.credentials_path = "credentials.txt"
        self.random_word = RandomWords()
        self.tbb_path = f'{Path.home()}/.local/opt/tor-browser/app/' # Add your own tor bundle path
        #self.cookiejar = browser_cookie3.firefox(domain_name="google.com")

    def generate_username(self):
        word = self.random_word.get_random_word()
        while word == None:
            word = self.random_word.get_random_word()
        return f"{word.split(' ')[0].replace('-', '')}{randrange(10000, 100000)}"

    def create_accounts(self):
        for i in range(5):
            usr = self.generate_username()
            pwd = self.pwd
            self.save_credentials(usr, pwd)
            self.create_account(usr, pwd)

    def save_credentials(self, usr, pwd):
        print(f"{usr};{pwd}")
        with open(self.credentials_path, "a") as f:
            f.write(f"{usr};{pwd}\n")

    def create_tor_bundle_driver(self):
        return TorBrowserDriver(self.tbb_path, socks_port=9150, tbb_logfile_path='/dev/null')

    def create_firefox_tor_driver(self):
        profile = FirefoxProfile(self.tbb_path + 'Browser/TorBrowser/Data/Browser/profile.default/')
        options = webdriver.FirefoxOptions()
        options.set_preference('network.proxy.type', 1)
        options.set_preference('network.proxy.socks_version', 5)
        options.set_preference('network.proxy.socks', '127.0.0.1')
        options.set_preference('network.proxy.socks_port', 9150)
        options.set_preference('network.proxy.socks_remote_dns', False)
        return webdriver.Firefox(firefox_profile=profile, options=options)

    def create_account(self, usr, pwd):
        driver = self.create_tor_bundle_driver()
        driver.delete_all_cookies()
        driver.get('https://www.reddit.com/register/')
        """ for c in self.cookiejar:
            driver.add_cookie({'name': c.name, 'value': c.value, 'path': c.path, 'expiry': c.expires}) """
        driver.find_element(by=By.ID, value="regEmail").send_keys(
            f"{usr}@gmail.com")
        driver.find_element(
            by=By.XPATH, value="//button[contains(text(),'Continue')]").click()
        time.sleep(2)
        driver.find_element(by=By.ID, value="regUsername").send_keys(usr)
        driver.find_element(by=By.ID, value="regPassword").send_keys(pwd)
        while driver.current_url != "https://www.reddit.com/":
            time.sleep(0.5)
        driver.close()


gen = AccountGenerator()
gen.create_accounts()
