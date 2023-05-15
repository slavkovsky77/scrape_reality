import os

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from scrapper.db import ScrappedFlat


def parse_yit_page(page=0):
    # Initialize the web driver
    chrome_options = webdriver.ChromeOptions()
    if 'USE_DOCKER_CHROME' in os.environ:
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options=chrome_options)

    # Navigate to the webpage
    url = (
        f"https://www.yit.sk/en/flats-for-sale/bratislava"
        f"?tab=apartments&sort=ReservationStatusIndex&order=asc&page={page}")
    driver.get(url)

    # Wait for the cookie banner to appear
    wait = WebDriverWait(driver, 5)
    cookie_banner = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "cc-cookiebanner")))

    # Wait for the accept all button to appear
    accept_all_button = cookie_banner.find_element(By.CSS_SELECTOR, "button[data-allowall='']")
    accept_all_button.click()

    # Scroll down to load all the elements
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    ActionChains(driver).pause(1).perform()

    flat_elements_second = driver.find_elements(By.XPATH, "//div[@class='grid-element__second']")
    flat_img_elements = driver.find_elements(By.XPATH, "//div[@class='grid-element__img']")
    flat_elements_first = driver.find_elements(By.XPATH, "//div[@class='grid-element__first']")
    flats = []

    zipped = zip(flat_elements_first, flat_elements_second, flat_img_elements)
    for flat_element_first, flat_element_second, flat_img_element in zipped:
        flat = ScrappedFlat()

        # Extract the title
        title_element = flat_element_second.find_element(By.XPATH, ".//h3[@class='grid-element__title']")
        title_text = title_element.find_element(By.XPATH, ".//span").text
        flat.title = title_text

        # Extract the apartment number
        apartment_number_element = flat_element_second.find_element(
            By.XPATH,
            ".//dt[text()='Apartment number']/following-sibling::dd")
        apartment_number_text = apartment_number_element.text
        flat.apartment_number = apartment_number_text

        # Extract the number of rooms
        rooms_element = flat_element_second.find_element(By.XPATH, ".//dt[text()='Rooms']/following-sibling::dd")
        rooms_text = rooms_element.text
        flat.rooms = rooms_text

        # Extract the size
        size_element = flat_element_second.find_element(By.XPATH, ".//dt[text()='Size']/following-sibling::dd")
        size_text = size_element.text
        flat.size = size_text

        # Extract the total area size
        total_area_size_element = flat_element_second.find_element(
            By.XPATH, ".//dt[text()='Total area size']/following-sibling::dd")
        total_area_size_text = total_area_size_element.text
        flat.total_area_size = total_area_size_text

        # Extract the sales price
        sales_price_element = flat_element_second.find_element(
            By.XPATH, ".//dt[text()='Sales price']/following-sibling::dd")
        sales_price_text = sales_price_element.text
        flat.sales_price = sales_price_text

        # Extract the floor number
        floor_number_element = flat_element_second.find_element(
            By.XPATH, ".//dt[text()='Floor number']/following-sibling::dd")
        floor_number_text = floor_number_element.text
        flat.floor_number = floor_number_text

        # Extract the project name
        project_name_element = flat_element_second.find_element(
            By.XPATH, ".//div[@class='grid-element__project-address']/strong")
        project_name_text = project_name_element.text
        flat.project_name = project_name_text

        # Extract the href
        href_element = flat_img_element.find_element(By.XPATH, ".//a")
        href_text = href_element.get_attribute("href")
        flat.href = href_text

        # Extract the image source URL
        img_element = flat_img_element.find_element(By.XPATH, ".//img")
        img_src_text = img_element.get_attribute("src")
        flat.img_src = img_src_text

        # Check if the flat is reserved
        try:
            status_element = flat_element_first.find_element(By.XPATH, ".//span[@class='status reserved']")
            status_text = status_element.text
            flat.status = status_text
        except NoSuchElementException:
            flat.status = 'Available'

        flats.append(flat)

    # Close the web driver
    driver.quit()

    return flats