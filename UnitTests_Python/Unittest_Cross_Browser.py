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

import HtmlTestRunner
# import AllureReports

class ChromeSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.maximize_window()

    def test_search_conditions_chrome(self):
        driver = self.driver
        driver.get('https://www.localconditions.com')

        wait = WebDriverWait(driver, 3)

        search = wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="weather-search-input-ind"]')))
        search.clear()
        search.send_keys("48130")
        driver.find_element(By.XPATH, '//input[@value="Go"]').click()
        time.sleep(random.randint(3, 5))

        # Check if the search is correct
        assert "Dexter, MI Current Weather Report in 48130 | LocalConditions" in driver.title
        print("Page title in conditions_test is:", driver.title)
        # Verify if the location selection is accurate.
        wait.until(EC.visibility_of_element_located((By.XPATH, "//h1[text() ='Dexter, MI Weather']")))
        print("TC 1.1 Selection of location is accurate.")

        logo = driver.find_element(By.XPATH, "//img[contains(@alt,'LocalConditions.com Logo')]")
        driver.execute_script("arguments[0].scrollIntoView(true)", logo)
        logo.click()
        print("TC 4.0 Logo is present and navigates to the website's homepage")

        time.sleep(random.randint(3, 5))
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
        print("TC 1.2 Selection of location is accurate.")

        # Check Weather frame functionality with "try-except"
        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, '//p[@class="row-stat-value"]')))
            print("Weather widget is visible")
        except TimeoutException:
            print("Weather widget loading took more than 2 sec")

        # Check Weather frame functionality with NO "try-except"
        wait.until(
            EC.visibility_of_element_located((By.XPATH, "//button[@type='button'][contains(.,'Listen to Report')]")))
        print("Listen to Report button is visible")
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='button'][contains(.,'Listen to Report')]")))
        print("Listen to Report button is clickable")
        listen = driver.find_element(By.XPATH, "//button[@type='button'][contains(.,'Listen to Report')]")
        driver.execute_script("arguments[0].scrollIntoView(true)", listen)
        listen.click()

        wait.until(EC.visibility_of_element_located((By.ID, 'readWx')))  # //button[@class='btn btn-sm default']
        print("Read button is visible")
        driver.find_element(By.ID, 'readWx').click()
        print("TC 2.0 Feature 'listen to report' is functional")
        listen.click()

        # Multi-Day Outlook
        day1 = driver.find_element(By.XPATH, '//a[@href="#dayoutlook1"]')
        driver.execute_script("arguments[0].scrollIntoView(true)", day1)
        driver.find_element(By.XPATH, "//div[@class='col-sm-2 col-md-2'][contains(.,'Low: ')]")
        wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="#dayoutlook2"]')))
        driver.find_element(By.XPATH, '//a[@href="#dayoutlook2"]').click()
        driver.find_element(By.XPATH, "//div[@class='col-sm-2 col-md-2'][contains(.,'High: ')]")
        wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="#dayoutlook3"]')))
        driver.find_element(By.XPATH, '//a[@href="#dayoutlook3"]').click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="#dayoutlook4"]')))
        driver.find_element(By.XPATH, '//a[@href="#dayoutlook4"]').click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="#dayoutlook5"]')))
        driver.find_element(By.XPATH, '//a[@href="#dayoutlook5"]').click()
        print("TC 3.0 The 'Multi-Day Outlook' module is functional")
        # Temperatures Today
        wait.until(EC.visibility_of_element_located((By.ID, 'temperature')))
        print("Hourly chart report is visible")

        # Check header menu
        traffic = driver.find_element(By.XPATH, '//a[contains(.,"Traffic Conditions")]')
        driver.execute_script("arguments[0].scrollIntoView(true)", traffic)
        traffic.click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//canvas[@class="mapboxgl-canvas"]')))
        print("TC 5.5 Traffic Conditions feature is functional")

        h_by_h = driver.find_element(By.XPATH, '//a[@title="Ann Arbor Hourly Weather Forecast"]')
        driver.execute_script("arguments[0].scrollIntoView(true)", h_by_h)
        h_by_h.click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//table[@class ="table table-bordered hourly_grid"]')))
        print("TC 5.7 'Hour By Hour' feature is functional")

        day5 = driver.find_element(By.XPATH, '//a[@title="Ann Arbor 5 Day Forecast"]')
        driver.execute_script("arguments[0].scrollIntoView(true)", day5)
        day5.click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//h1[contains(.," 5 Day Forecast")]')))
        print("TC 5.9 '5 Day Forecast' feature is functional")

        radar = driver.find_element(By.XPATH, '//a[@title="Ann Arbor Radar Weather Maps"]')
        driver.execute_script("arguments[0].scrollIntoView(true)", radar)
        radar.click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//img[@alt="Base Reflectivity loop"]')))
        print("TC 5.11 'Radar' feature is functional")

        warnings = driver.find_element(By.XPATH, '//a[contains(.,"Warnings and Advisories")]')
        driver.execute_script("arguments[0].scrollIntoView(true)", warnings)
        warnings.click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//h1[contains(.," Warnings, Watches and Advisories")]')))
        print("TC 5.13 'Warnings and Advisories' feature is functional")

        past = driver.find_element(By.XPATH, '//a[@title="Ann Arbor Past Weather"]')
        driver.execute_script("arguments[0].scrollIntoView(true)", past)
        past.click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='#day0']")))
        print("TC 5.15 'Past' feature is functional")

        # Negative test cases
        time.sleep(random.randint(3, 5))
        logo = driver.find_element(By.XPATH, "//img[@alt='Local Weather, Weather Forecast, Traffic Reports']")
        driver.execute_script("arguments[0].scrollIntoView(true)", logo)
        logo.click()
        time.sleep(random.randint(3, 5))
        search = wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="weather-search-input-ind"]')))
        search.clear()
        search.send_keys("98765")
        driver.find_element(By.XPATH, '//input[@value="Go"]').click()
        time.sleep(random.randint(3, 5))

        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, '//h4[contains(.," was not found!")]')))
            print('TC 7.0 The message "We are sorry, the location or page you selected was not found!" appeared')
        except TimeoutException:
            print("Loading text too much time!")
        # element = driver.find_element(By.PARTIAL_LINK_TEXT, "//span[contains(.,'the location or page you selected')]")
        if 'the location or page you selected' in driver.page_source:
            print("TC 7.0 Status PASS")
        else:
            print("TC 7.0 " + driver.title)
            print("TC 7.0 Status FAIL")

        # Special characters input
        time.sleep(random.randint(3, 5))
        logo = driver.find_element(By.XPATH, "//img[@alt='Local Weather, Weather Forecast, Traffic Reports']")
        driver.execute_script("arguments[0].scrollIntoView(true)", logo)
        logo.click()
        time.sleep(random.randint(3, 5))
        search = wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="weather-search-input-ind"]')))
        search.clear()
        search.send_keys("!@#$%^")
        driver.find_element(By.XPATH, '//input[@value="Go"]').click()
        time.sleep(random.randint(3, 5))

        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, '//h4[contains(.," was not found!")]')))
            print('TC 8.0 The message "We are sorry, the location or page you selected was not found!" appeared')
        except TimeoutException:
            print("TC 8.0 Loading page too much time!")

        if 'the location or page you selected' in driver.page_source:
            print("TC 8.0 Status PASS")
        else:
            print('TC 8.0 ' + driver.title)
            print("TC 8.0 Status FAIL")


    def test_mobile_conditions_chrome_390x844(self):
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

        # Check if the search returns correct result
        assert "No results found." not in driver.page_source, "No results found in Chrome"
        assert "Ann Arbor, MI Current Weather Report in 48103 | LocalConditions" in driver.title
        print("Weather_chrome_390x844 test title is:", driver.title)
        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, '//h1[contains(.,"Ann Arbor, MI Weather")]')))
        except NoSuchElementException:
            print("Widget title invisible (390x844)")

        # Check hamburger menu
        menu = driver.find_element(By.XPATH, '// i[@ class ="fa fa-bars"]')
        menu.click()
        time.sleep(random.randint(3, 5))
        driver.find_element(By.XPATH, '//a[contains(.,"Traffic Conditions")]').click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//canvas[@class="mapboxgl-canvas"]')))
        print("TC 6.5 Traffic Conditions feature is functional")

        menu = driver.find_element(By.XPATH, '// i[@ class ="fa fa-bars"]')
        menu.click()
        driver.find_element(By.XPATH, '//a[@title="Ann Arbor Hourly Weather Forecast"]').click()
        time.sleep(random.randint(3, 5))
        '''
        try:     # Close ad window
            wait.until(EC.visibility_of_element_located((By.ID, "dismiss-button")))
            print('"Close" button is visible')
            wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@id="dismiss-button"]')))
            print('"Close" button is clickable')
            driver.find_element(By.ID, "dismiss-button").click()
            print('Ad window closed')
        except TimeoutException:
            print('Timeout while waiting for "dismiss-button"')'''

        wait.until(EC.element_to_be_clickable((By.XPATH, '//table[@class ="table table-bordered hourly_grid"]')))
        print("TC 6.7 'Hour By Hour' feature is functional")

        menu = driver.find_element(By.XPATH, '// i[@ class ="fa fa-bars"]')
        menu.click()
        driver.find_element(By.XPATH, '//a[@title="Ann Arbor 5 Day Forecast"]').click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//h1[contains(.," 5 Day Forecast")]')))
        print("TC 6.9 '5 Day Forecast' feature is functional")

        menu = driver.find_element(By.XPATH, '// i[@ class ="fa fa-bars"]')
        menu.click()
        driver.find_element(By.XPATH, '//a[@title="Ann Arbor Radar Weather Maps"]').click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//img[@alt="Base Reflectivity loop"]')))
        print("TC 6.11 'Radar' feature is functional")

        menu = driver.find_element(By.XPATH, '// i[@ class ="fa fa-bars"]')
        menu.click()
        time.sleep(random.randint(3, 5))
        driver.find_element(By.XPATH, '//a[contains(.,"Warnings and Advisories")]').click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//h1[contains(.," Warnings, Watches and Advisories")]')))
        print("TC 6.13 'Warnings and Advisories' feature is functional")

        menu = driver.find_element(By.XPATH, '// i[@ class ="fa fa-bars"]')
        menu.click()
        time.sleep(random.randint(3, 5))
        driver.find_element(By.XPATH, '//a[@title="Ann Arbor Past Weather"]').click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='#day0']")))
        print("TC 6.15 'Past' feature is functional")
        print("Hamburger menu is clickable")


    def tearDown(self):
        self.driver.quit()


class EdgeSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))
        self.driver.maximize_window()

    def test_search_conditions_edge(self):
        driver = self.driver
        driver.get('https://www.localconditions.com')

        wait = WebDriverWait(driver, 3)

        search = wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="weather-search-input-ind"]')))
        search.clear()
        search.send_keys("48130")
        driver.find_element(By.XPATH, '//input[@value="Go"]').click()
        time.sleep(random.randint(3, 5))

        # Check if the search is correct
        assert "Dexter, MI Current Weather Report in 48130 | LocalConditions" in driver.title
        print("Page title in conditions_test is:", driver.title)
        # Verify if the location selection is accurate.
        wait.until(EC.visibility_of_element_located((By.XPATH, "//h1[text() ='Dexter, MI Weather']")))
        print("TC 1.1 Selection of location is accurate.")

        logo = driver.find_element(By.XPATH, "//img[contains(@alt,'LocalConditions.com Logo')]")
        driver.execute_script("arguments[0].scrollIntoView(true)", logo)
        logo.click()
        print("TC 4.0 Logo is present and navigates to the website's homepage")

        time.sleep(random.randint(3, 5))
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
        print("TC 1.2 Selection of location is accurate.")

        # Check Weather frame functionality with "try-except"
        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, '//p[@class="row-stat-value"]')))
            print("Weather widget is visible")
        except TimeoutException:
            print("Weather widget loading took more than 2 sec")

        # Check Weather frame functionality with NO "try-except"
        wait.until(
            EC.visibility_of_element_located((By.XPATH, "//button[@type='button'][contains(.,'Listen to Report')]")))
        print("Listen to Report button is visible")
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='button'][contains(.,'Listen to Report')]")))
        print("Listen to Report button is clickable")
        listen = driver.find_element(By.XPATH, "//button[@type='button'][contains(.,'Listen to Report')]")
        driver.execute_script("arguments[0].scrollIntoView(true)", listen)
        listen.click()

        wait.until(EC.visibility_of_element_located((By.ID, 'readWx')))  # //button[@class='btn btn-sm default']
        print("Read button is visible")
        driver.find_element(By.ID, 'readWx').click()
        print("TC 2.0 Feature 'listen to report' is functional")
        listen.click()
        # driver.find_element(By.XPATH, "//button[@type='button'][contains(.,'Listen to Report')]").click()
        # Multi-Day Outlook
        day1 = driver.find_element(By.XPATH, '//a[@href="#dayoutlook1"]')
        driver.execute_script("arguments[0].scrollIntoView(true)", day1)
        driver.find_element(By.XPATH, "//div[@class='col-sm-2 col-md-2'][contains(.,'Low: ')]")
        wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="#dayoutlook2"]')))
        driver.find_element(By.XPATH, '//a[@href="#dayoutlook2"]').click()
        driver.find_element(By.XPATH, "//div[@class='col-sm-2 col-md-2'][contains(.,'High: ')]")
        wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="#dayoutlook3"]')))
        driver.find_element(By.XPATH, '//a[@href="#dayoutlook3"]').click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="#dayoutlook4"]')))
        driver.find_element(By.XPATH, '//a[@href="#dayoutlook4"]').click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="#dayoutlook5"]')))
        driver.find_element(By.XPATH, '//a[@href="#dayoutlook5"]').click()
        print("TC 3.0 The 'Multi-Day Outlook' module is functional")
        # Temperatures Today
        wait.until(EC.visibility_of_element_located((By.ID, 'temperature')))
        print("Hourly chart report is visible")

        # Check header menu
        traffic = driver.find_element(By.XPATH, '//a[contains(.,"Traffic Conditions")]')
        driver.execute_script("arguments[0].scrollIntoView(true)", traffic)
        traffic.click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//canvas[@class="mapboxgl-canvas"]')))
        print("TC 5.5 Traffic Conditions feature is functional")

        h_by_h = driver.find_element(By.XPATH, '//a[@title="Ann Arbor Hourly Weather Forecast"]')
        driver.execute_script("arguments[0].scrollIntoView(true)", h_by_h)
        h_by_h.click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//table[@class ="table table-bordered hourly_grid"]')))
        print("TC 5.7 'Hour By Hour' feature is functional")

        day5 = driver.find_element(By.XPATH, '//a[@title="Ann Arbor 5 Day Forecast"]')
        driver.execute_script("arguments[0].scrollIntoView(true)", day5)
        day5.click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//h1[contains(.," 5 Day Forecast")]')))
        print("TC 5.9 '5 Day Forecast' feature is functional")

        radar = driver.find_element(By.XPATH, '//a[@title="Ann Arbor Radar Weather Maps"]')
        driver.execute_script("arguments[0].scrollIntoView(true)", radar)
        radar.click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//img[@alt="Base Reflectivity loop"]')))
        print("TC 5.11 'Radar' feature is functional")

        warnings = driver.find_element(By.XPATH, '//a[contains(.,"Warnings and Advisories")]')
        driver.execute_script("arguments[0].scrollIntoView(true)", warnings)
        warnings.click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//h1[contains(.," Warnings, Watches and Advisories")]')))
        print("TC 5.13 'Warnings and Advisories' feature is functional")

        past = driver.find_element(By.XPATH, '//a[@title="Ann Arbor Past Weather"]')
        driver.execute_script("arguments[0].scrollIntoView(true)", past)
        past.click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='#day0']")))
        print("TC 5.15 'Past' feature is functional")

        # Negative test cases
        time.sleep(random.randint(3, 5))
        logo = driver.find_element(By.XPATH, "//img[@alt='Local Weather, Weather Forecast, Traffic Reports']")
        driver.execute_script("arguments[0].scrollIntoView(true)", logo)
        logo.click()
        time.sleep(random.randint(3, 5))
        search = wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="weather-search-input-ind"]')))
        search.clear()
        search.send_keys("98765")
        driver.find_element(By.XPATH, '//input[@value="Go"]').click()
        time.sleep(random.randint(3, 5))

        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, '//h4[contains(.," was not found!")]')))
            print('TC 7.0 The message "We are sorry, the location or page you selected was not found!" appeared')
        except TimeoutException:
            print("Loading text too much time!")
        # element = driver.find_element(By.PARTIAL_LINK_TEXT, "//span[contains(.,'the location or page you selected')]")
        if 'the location or page you selected' in driver.page_source:
            print("TC 7.0 Status PASS")
        else:
            print("TC 7.0 " + driver.title)
            print("TC 7.0 Status FAIL")

        # Special characters input
        time.sleep(random.randint(3, 5))
        logo = driver.find_element(By.XPATH, "//img[@alt='Local Weather, Weather Forecast, Traffic Reports']")
        driver.execute_script("arguments[0].scrollIntoView(true)", logo)
        logo.click()
        time.sleep(random.randint(3, 5))
        search = wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="weather-search-input-ind"]')))
        search.clear()
        search.send_keys("!@#$%^")
        driver.find_element(By.XPATH, '//input[@value="Go"]').click()
        time.sleep(random.randint(3, 5))

        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, '//h4[contains(.," was not found!")]')))
            print('TC 8.0 The message "We are sorry, the location or page you selected was not found!" appeared')
        except TimeoutException:
            print("TC 8.0 Loading page too much time!")

        if 'the location or page you selected' in driver.page_source:
            print("TC 8.0 Status PASS")
        else:
            print('TC 8.0 ' + driver.title)
            print("TC 8.0 Status FAIL")


    def test_mobile_conditions_edge_390x844(self):
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

        # Check if the search returns correct result
        assert "No results found." not in driver.page_source, "No results found in Chrome"
        assert "Ann Arbor, MI Current Weather Report in 48103 | LocalConditions" in driver.title
        print("Weather_chrome_390x844 test title is:", driver.title)
        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, '//h1[contains(.,"Ann Arbor, MI Weather")]')))
        except NoSuchElementException:
            print("Widget title invisible (390x844)")

        # Check hamburger menu
        menu = driver.find_element(By.XPATH, '// i[@ class ="fa fa-bars"]')
        menu.click()
        time.sleep(random.randint(3, 5))
        driver.find_element(By.XPATH, '//a[contains(.,"Traffic Conditions")]').click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//canvas[@class="mapboxgl-canvas"]')))
        print("TC 6.5 Traffic Conditions feature is functional")

        menu = driver.find_element(By.XPATH, '// i[@ class ="fa fa-bars"]')
        menu.click()
        driver.find_element(By.XPATH, '//a[@title="Ann Arbor Hourly Weather Forecast"]').click()
        time.sleep(random.randint(3, 5))

        # driver.find_element(By.XPATH, '//a[@title="Ann Arbor Hourly Weather Forecast"]').click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//table[@class ="table table-bordered hourly_grid"]')))
        print("TC 6.7 'Hour By Hour' feature is functional")

        menu = driver.find_element(By.XPATH, '// i[@ class ="fa fa-bars"]')
        menu.click()
        driver.find_element(By.XPATH, '//a[@title="Ann Arbor 5 Day Forecast"]').click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//h1[contains(.," 5 Day Forecast")]')))
        print("TC 6.9 '5 Day Forecast' feature is functional")

        menu = driver.find_element(By.XPATH, '// i[@ class ="fa fa-bars"]')
        menu.click()
        driver.find_element(By.XPATH, '//a[@title="Ann Arbor Radar Weather Maps"]').click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//img[@alt="Base Reflectivity loop"]')))
        print("TC 6.11 'Radar' feature is functional")

        menu = driver.find_element(By.XPATH, '// i[@ class ="fa fa-bars"]')
        menu.click()
        time.sleep(random.randint(3, 5))
        driver.find_element(By.XPATH, '//a[contains(.,"Warnings and Advisories")]').click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//h1[contains(.," Warnings, Watches and Advisories")]')))
        print("TC 6.13 'Warnings and Advisories' feature is functional")

        menu = driver.find_element(By.XPATH, '// i[@ class ="fa fa-bars"]')
        menu.click()
        time.sleep(random.randint(3, 5))
        driver.find_element(By.XPATH, '//a[@title="Ann Arbor Past Weather"]').click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='#day0']")))
        print("TC 6.15 'Past' feature is functional")
        print("Hamburger menu is clickable")


    def tearDown(self):
        self.driver.quit()


class FirefoxSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
        self.driver.maximize_window()

    def test_search_conditions_firefox(self):
        driver = self.driver
        driver.get('https://www.localconditions.com')

        wait = WebDriverWait(driver, 3)

        search = wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="weather-search-input-ind"]')))
        search.clear()
        search.send_keys("48130")
        driver.find_element(By.XPATH, '//input[@value="Go"]').click()
        time.sleep(random.randint(3, 5))

        # Check if the search is correct
        assert "Dexter, MI Current Weather Report in 48130 | LocalConditions" in driver.title
        print("Page title in conditions_test is:", driver.title)
        # Verify if the location selection is accurate.
        wait.until(EC.visibility_of_element_located((By.XPATH, "//h1[text() ='Dexter, MI Weather']")))
        print("TC 1.1 Selection of location is accurate.")

        logo = driver.find_element(By.XPATH, "//img[contains(@alt,'LocalConditions.com Logo')]")
        driver.execute_script("arguments[0].scrollIntoView(true)", logo)
        logo.click()
        print("TC 4.0 Logo is present and navigates to the website's homepage")

        time.sleep(random.randint(3, 5))
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
        print("TC 1.2 Selection of location is accurate.")

        # Check Weather frame functionality with "try-except"
        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, '//p[@class="row-stat-value"]')))
            print("Weather widget is visible")
        except TimeoutException:
            print("Weather widget loading took more than 2 sec")

        # Check Weather frame functionality with NO "try-except"
        wait.until(
            EC.visibility_of_element_located((By.XPATH, "//button[@type='button'][contains(.,'Listen to Report')]")))
        print("Listen to Report button is visible")
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='button'][contains(.,'Listen to Report')]")))
        print("Listen to Report button is clickable")
        listen = driver.find_element(By.XPATH, "//button[@type='button'][contains(.,'Listen to Report')]")
        driver.execute_script("arguments[0].scrollIntoView(true)", listen)
        listen.click()

        wait.until(EC.visibility_of_element_located((By.ID, 'readWx')))  # //button[@class='btn btn-sm default']
        print("Read button is visible")
        driver.find_element(By.ID, 'readWx').click()
        print("TC 2.0 Feature 'listen to report' is functional")
        driver.execute_script("arguments[0].scrollIntoView(true)", listen)
        listen.click()
        # driver.find_element(By.XPATH, "//button[@type='button'][contains(.,'Listen to Report')]").click()
        # Multi-Day Outlook
        day1 = driver.find_element(By.XPATH, '//a[@href="#dayoutlook1"]')
        driver.execute_script("arguments[0].scrollIntoView(true)", day1)
        driver.find_element(By.XPATH, "//div[@class='col-sm-2 col-md-2'][contains(.,'Low: ')]")
        wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="#dayoutlook2"]')))
        driver.find_element(By.XPATH, '//a[@href="#dayoutlook2"]').click()
        driver.find_element(By.XPATH, "//div[@class='col-sm-2 col-md-2'][contains(.,'High: ')]")
        wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="#dayoutlook3"]')))
        driver.find_element(By.XPATH, '//a[@href="#dayoutlook3"]').click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="#dayoutlook4"]')))
        driver.find_element(By.XPATH, '//a[@href="#dayoutlook4"]').click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="#dayoutlook5"]')))
        driver.find_element(By.XPATH, '//a[@href="#dayoutlook5"]').click()
        print("TC 3.0 The 'Multi-Day Outlook' module is functional")
        # Temperatures Today
        wait.until(EC.visibility_of_element_located((By.ID, 'temperature')))
        print("Hourly chart report is visible")

        # Check header menu
        traffic = driver.find_element(By.XPATH, '//a[contains(.,"Traffic Conditions")]')
        driver.execute_script("arguments[0].scrollIntoView(true)", traffic)
        traffic.click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//canvas[@class="mapboxgl-canvas"]')))
        print("TC 5.5 Traffic Conditions feature is functional")

        h_by_h = driver.find_element(By.XPATH, '//a[@title="Ann Arbor Hourly Weather Forecast"]')
        driver.execute_script("arguments[0].scrollIntoView(true)", h_by_h)
        h_by_h.click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//table[@class ="table table-bordered hourly_grid"]')))
        print("TC 5.7 'Hour By Hour' feature is functional")

        day5 = driver.find_element(By.XPATH, '//a[@title="Ann Arbor 5 Day Forecast"]')
        driver.execute_script("arguments[0].scrollIntoView(true)", day5)
        day5.click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//h1[contains(.," 5 Day Forecast")]')))
        print("TC 5.9 '5 Day Forecast' feature is functional")

        radar = driver.find_element(By.XPATH, '//a[@title="Ann Arbor Radar Weather Maps"]')
        driver.execute_script("arguments[0].scrollIntoView(true)", radar)
        radar.click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//img[@alt="Base Reflectivity loop"]')))
        print("TC 5.11 'Radar' feature is functional")

        warnings = driver.find_element(By.XPATH, '//a[contains(.,"Warnings and Advisories")]')
        driver.execute_script("arguments[0].scrollIntoView(true)", warnings)
        warnings.click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//h1[contains(.," Warnings, Watches and Advisories")]')))
        print("TC 5.13 'Warnings and Advisories' feature is functional")

        past = driver.find_element(By.XPATH, '//a[@title="Ann Arbor Past Weather"]')
        driver.execute_script("arguments[0].scrollIntoView(true)", past)
        past.click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='#day0']")))
        print("TC 5.15 'Past' feature is functional")

        # Negative test cases
        time.sleep(random.randint(3, 5))
        logo = driver.find_element(By.XPATH, "//img[@alt='Local Weather, Weather Forecast, Traffic Reports']")
        driver.execute_script("arguments[0].scrollIntoView(true)", logo)
        logo.click()
        time.sleep(random.randint(3, 5))
        search = wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="weather-search-input-ind"]')))
        search.clear()
        search.send_keys("98765")
        driver.find_element(By.XPATH, '//input[@value="Go"]').click()
        time.sleep(random.randint(3, 5))

        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, '//h4[contains(.," was not found!")]')))
            print('TC 7.0 The message "We are sorry, the location or page you selected was not found!" appeared')
        except TimeoutException:
            print("Loading text too much time!")
        # element = driver.find_element(By.PARTIAL_LINK_TEXT, "//span[contains(.,'the location or page you selected')]")
        if 'the location or page you selected' in driver.page_source:
            print("TC 7.0 Status PASS")
        else:
            print("TC 7.0 " + driver.title)
            print("TC 7.0 Status FAIL")

        # Special characters input
        time.sleep(random.randint(3, 5))
        logo = driver.find_element(By.XPATH, "//img[@alt='Local Weather, Weather Forecast, Traffic Reports']")
        driver.execute_script("arguments[0].scrollIntoView(true)", logo)
        logo.click()
        time.sleep(random.randint(3, 5))
        search = wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="weather-search-input-ind"]')))
        search.clear()
        search.send_keys("!@#$%^")
        driver.find_element(By.XPATH, '//input[@value="Go"]').click()
        time.sleep(random.randint(3, 5))

        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, '//h4[contains(.," was not found!")]')))
            print('TC 8.0 The message "We are sorry, the location or page you selected was not found!" appeared')
        except TimeoutException:
            print("TC 8.0 Loading page too much time!")

        if 'the location or page you selected' in driver.page_source:
            print("TC 8.0 Status PASS")
        else:
            print('TC 8.0 ' + driver.title)
            print("TC 8.0 Status FAIL")


    def test_mobile_conditions_firefox_390x844(self):
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

        # Check if the search returns correct result
        assert "No results found." not in driver.page_source, "No results found in Chrome"
        assert "Ann Arbor, MI Current Weather Report in 48103 | LocalConditions" in driver.title
        print("Weather_chrome_390x844 test title is:", driver.title)
        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, '//h1[contains(.,"Ann Arbor, MI Weather")]')))
        except NoSuchElementException:
            print("Widget title invisible (390x844)")

        # Check hamburger menu
        menu = driver.find_element(By.XPATH, '// i[@ class ="fa fa-bars"]')
        menu.click()
        time.sleep(random.randint(3, 5))
        driver.find_element(By.XPATH, '//a[contains(.,"Traffic Conditions")]').click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//canvas[@class="mapboxgl-canvas"]')))
        print("TC 6.5 Traffic Conditions feature is functional")

        menu = driver.find_element(By.XPATH, '// i[@ class ="fa fa-bars"]')
        menu.click()
        driver.find_element(By.XPATH, '//a[@title="Ann Arbor Hourly Weather Forecast"]').click()
        time.sleep(random.randint(3, 5))

        wait.until(EC.element_to_be_clickable((By.XPATH, '//table[@class ="table table-bordered hourly_grid"]')))
        print("TC 6.7 'Hour By Hour' feature is functional")

        menu = driver.find_element(By.XPATH, '// i[@ class ="fa fa-bars"]')
        menu.click()
        driver.find_element(By.XPATH, '//a[@title="Ann Arbor 5 Day Forecast"]').click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//h1[contains(.," 5 Day Forecast")]')))
        print("TC 6.9 '5 Day Forecast' feature is functional")

        menu = driver.find_element(By.XPATH, '// i[@ class ="fa fa-bars"]')
        menu.click()
        radar = driver.find_element(By.XPATH, '//a[@title="Ann Arbor Radar Weather Maps"]')
        driver.execute_script("arguments[0].scrollIntoView(true)", radar)
        radar.click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//img[@alt="Base Reflectivity loop"]')))
        print("TC 6.11 'Radar' feature is functional")

        menu = driver.find_element(By.XPATH, '// i[@ class ="fa fa-bars"]')
        menu.click()
        time.sleep(random.randint(3, 5))
        driver.find_element(By.XPATH, '//a[contains(.,"Warnings and Advisories")]').click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//h1[contains(.," Warnings, Watches and Advisories")]')))
        print("TC 6.13 'Warnings and Advisories' feature is functional")

        menu = driver.find_element(By.XPATH, '// i[@ class ="fa fa-bars"]')
        menu.click()
        time.sleep(random.randint(3, 5))
        driver.find_element(By.XPATH, '//a[@title="Ann Arbor Past Weather"]').click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='#day0']")))
        print("TC 6.15 'Past' feature is functional")
        print("Hamburger menu is clickable")


    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='C:/Users/Sergey/WORK/Selenium/HtmlReports'))