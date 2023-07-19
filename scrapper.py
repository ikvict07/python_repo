from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Scrapper:

    def __init__(self):
        self.driver = None
        self.options = None


    def configure_options(self):
        # configure Chrome options
        self.options = Options()
        self.options.add_argument('--headless')
        return self

    def configure_driver(self):
        # Use the Chrome browser with specific driver and added options
        self.driver = webdriver.Chrome(r"C:\Users\ikvict\Downloads\chromedriver.exe", options=self.options)
        return self

    @staticmethod
    def __provide_url(self, url):
        self.driver.get(url)
        return self

    def __find_logic(self):

        # Wait for the necessary element to load
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "p.text-md.font-semibold.text-center")))

        html = self.driver.page_source

        soup = BeautifulSoup(html, 'html.parser')

        data = soup.find('p', class_='text-md font-semibold text-center')
        if data is not None:
            print(data.text)
        else:
            print("Required HTML element is not present in the page.")

    def find(self, url):
        self.configure_options().configure_driver().__provide_url(self, url).__find_logic()


scrapper = Scrapper()
for i in range(15):
    scrapper.find("https://apespace.io/bsc/0x21597370c2b598c4e781bb7368fddeaaabb38789")
