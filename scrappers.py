from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromiumService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from selenium.webdriver.support.ui import WebDriverWait
import requests
from bs4 import BeautifulSoup


class Scrapper():
    def __init__(self, url, **kwargs) -> None:
        self.url = url

    def scrap(self):
        return "Should be initialized by subclass"

class Bs4Scrapper(Scrapper):
    def scrap(self):
        """
        get all the text of a static webpage from the url, does not work with dynamic webpages (e.g. javascript excecuted)
        """
        headers = { 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0' }
        html = requests.get(self.url, headers=headers).text
        soup = BeautifulSoup(html, features="html.parser")
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        return '\n'.join(line for line in lines if line)

class SeleniumScrapper(Scrapper):
    def scrap(self):
        driver = webdriver.Chrome(service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()))
        # Setup Selenium WebDriver
        # Open the webpage
        self.driver.get(self.url)
        # Wait for JavaScript to load (if necessary)
        WebDriverWait(driver, 10).until(lambda d: d.execute_script('return jQuery.active == 0'))
        # Extract all text from the webpage
        text = driver.find_element(By.TAG_NAME, 'body').text
        driver.quit()
        return text