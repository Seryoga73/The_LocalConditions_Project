from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
import random
import unittest
import time
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.edge.service import Service
# import HtmlTestRunner
import AllureReports

class ChromeSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.maximize_window()

    def test_search_conditions_chrome(self):
        driver = self.driver
        driver.get('https://www.localconditions.com')

        wait = WebDriverWait(driver, 2)
        
        search = wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="weather-search-input-ind"]')))
        search.clear()
        search.send_keys("Ann Arbor, MI")
        driver.find_element(By.XPATH, '//input[@value="Go"]').click()
        time.sleep(random.randint(3, 5))

        # Check if the search is correct
        assert "Ann Arbor, MI Current Weather Report in 48103 | LocalConditions" in driver.title
        print("Page title in conditions_test is:", driver.title)

        # Verify if the location selection is accurate.
        wait.until(EC.visibility_of_element_located((By.XPATH, "//h1[text() ='Ann Arbor, MI Weather']")))
        print("Selection of location is accurate.")

        # Check Weather frame functionality with "try-except"
        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, '//p[@class="row-stat-value"]')))
            print("Weather widget is visible")
        except TimeoutException:
            print("Weather widget loading took more than 2 sec")

        # Check Weather frame functionality with NO "try-except"
        wait.until(EC.visibility_of_element_located((By.XPATH, "//button[@type='button'][contains(.,'Listen to Report')]")))
        print("Listen to Report button is visible")
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='button'][contains(.,'Listen to Report')]")))
        print("Listen to Report button is clickable")
        listen = driver.find_element(By.XPATH, "//button[@type='button'][contains(.,'Listen to Report')]")
        listen.send_keys(Keys.PAGE_DOWN)
        listen.click()

        wait.until(EC.visibility_of_element_located((By.ID, 'readWx')))  # //button[@class='btn btn-sm default']
        print("Read button is visible")
        wait.until(EC.element_to_be_clickable((By.ID, 'readWx')))
        print("Read button is clickable")
        listen.click()
        #driver.find_element(By.XPATH, "//button[@type='button'][contains(.,'Listen to Report')]").click()
        # Multi-Day Outlook
        wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="#dayoutlook2"]')))
        print("TUES button is clickable")
        wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="#dayoutlook3"]')))
        print("WED button is clickable")
        wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="#dayoutlook4"]')))
        print("THUR button is clickable")
        wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="#dayoutlook5"]')))
        print("FRI button is clickable")
        # Temperatures Today
        wait.until(EC.visibility_of_element_located((By.ID, 'temperature')))
        print("Hourly chart report is visible")

        # Check header menu
        wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@title="Ann Arbor Hourly Weather Forecast"]')))
        print("Hour By Hour button is clickable")
        
        wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@title="Ann Arbor 5 Day Forecast"]')))
        print("5 Day Forecast button is clickable")
        wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@title="Ann Arbor Radar Weather Maps"]')))
        print("Radar button is clickable")
        wait.until(EC.element_to_be_clickable((By.XPATH, '//a[contains(.,"Warnings and Advisories")]')))
        print("Warnings and Advisories button is clickable")
        wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@title="Ann Arbor Past Weather"]')))
        print("Past button is clickable")
        wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@title="Ann Arbor Traffic"]')))
        print("Traffic Conditions button is clickable")

        wait.until(EC.visibility_of_element_located((By.XPATH, '//img[@src="images/local-conditions-logo-ind.png"]')))
        time.sleep(random.randint(3, 5)) 

    def test_mobile_traffic_chrome_390x844(self):
        driver = self.driver
        driver.set_window_size(390, 844) # Dimension: IPhone 12 PRO
        driver.get('https://www.localconditions.com')
        wait = WebDriverWait(driver, 5)
        wait.until(EC.visibility_of_element_located((By.XPATH, "//img[@src='images/local-conditions-logo-ind.png']")))
        time.sleep(random.randint(3, 5))

        search = driver.find_element(By.XPATH, "//input[@class='weather-search-input-ind']")
        search.clear()
        search.send_keys("Ann Arbor, MI")
        driver.find_element(By.XPATH, '//input[@value="Go"]').click()
        time.sleep(random.randint(3, 5))

        driver.find_element(By.XPATH, '// i[@ class ="fa fa-bars"]').click()
        print("Sandwich bar menu is clickable")
        wait.until(EC.visibility_of_element_located((By.XPATH, "//a[@title='Ann Arbor Traffic']")))
        driver.find_element(By.XPATH, "//a[@title='Ann Arbor Traffic']").click()
        print("Traffic Conditions button is clickable")
        wait.until(EC.visibility_of_element_located((By.XPATH, "//h1[contains(.,'Ann Arbor Traffic and Road Conditions')]")))
        print("Title is present")
        # Check if the page title is correct
        assert "Ann Arbor Road Conditions with Driving and Traffic Flow - LocalConditions.com" in driver.title
        print("Traffic_chrome_390x844 test title is:", driver.title)

        # Check Traffic frame functionality with "try-except" and TimeoutException
        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[contains(.,'Ann Arbor Traffic Map')]")))
            wait.until(EC.element_to_be_clickable((By.XPATH, "//canvas[@aria-label='Map']")))
            wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(.,'Map and Alerts Usage Tips and FAQs')]")))
            wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(.,'Official Michigan DOT Road Conditions site')]")))
            wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@title='Full Weather Report and Forecast for Ann Arbor, MI']")))
            wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@title='Ann Arbor Rader Maps']")))
            wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@title='Ann Arbor Daily Charts']")))
            wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(.,'Ann Arbor, MI Past Weather')]")))
        except TimeoutException:
            print("Weather widget loading took more than 5 sec")

    def test_mobile_weather_chrome_390x844(self):
        driver = self.driver
        driver.set_window_size(390, 844)
        driver.get('https://www.localconditions.com')
        wait = WebDriverWait(driver, 5)
        wait.until(EC.visibility_of_element_located((By.XPATH, "//img[@src='images/local-conditions-logo-ind.png']")))
        time.sleep(random.randint(3, 5))

        search = driver.find_element(By.XPATH, "//input[@class='weather-search-input-ind']")
        search.clear()
        search.send_keys("Ann Arbor, MI")
        driver.find_element(By.XPATH, '//input[@value="Go"]').click()
        time.sleep(random.randint(3, 5))

        # Check if the search returns any result
        assert "No results found." not in driver.page_source, "No results found in Chrome"
        assert "Ann Arbor, MI Current Weather Report in 48103 | LocalConditions" in driver.title
        print("Weather_chrome_390x844 test title is:", driver.title)

        # Check Weather frame functionality with "try-except" and NoSuchElementException
        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, '//h1[contains(.,"Ann Arbor, MI Weather")]')))
        except NoSuchElementException:
            print("Widget title in invisible (390x844)")

            wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@class="btn btn-info"]')))
            print("Listen to Report button is visible")
            driver.find_element(By.XPATH, '//button[@class="btn btn-info"]').click()
            wait.until(EC.visibility_of_element_located((By.ID, 'readWx')))
            print("Read button is visible")
            wait.until(EC.element_to_be_clickable((By.ID, 'readWx')))
            print("Read button is clickable")
            driver.find_element(By.XPATH, '//button[@class="btn btn-info"]').click()
            # Multi-Day Outlook
            wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="#dayoutlook2"]')))
            print("TUES button is clickable")
            wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="#dayoutlook3"]')))
            print("WED button is clickable")
            wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="#dayoutlook4"]')))
            print("THUR button is clickable")
            wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="#dayoutlook5"]')))
            print("FRI button is clickable")
            wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="#dayoutlook1"]')))
            print("MON button is clickable")
            # Temperatures Today
            wait.until(EC.visibility_of_element_located((By.ID, 'temperature')))
            print("Hourly chart report is visible")

    def tearDown(self):
        self.driver.quit()
