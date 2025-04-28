import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(scope="module")
def driver():
    """
    Initializes and yields a Microsoft Edge WebDriver instance with specified options.
    This function configures the WebDriver to run in headless mode and disables GPU usage 
    for compatibility and performance purposes. It is intended to be used as a fixture 
    or context manager to manage the WebDriver's lifecycle.
    Yields:
        Edge WebDriver: A configured instance of the Microsoft Edge WebDriver.
    """

    options = webdriver.EdgeOptions()
    #options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Edge(options=options)

    yield driver

def test_python_org_search(driver, record_screen):
    """
    Tests the search functionality on the Python.org website.

    This test navigates to the Python.org homepage, verifies the page title,
    performs a search for the term "pycon", and asserts that results are found.

    Args:
        driver (WebDriver): The Selenium WebDriver instance used to interact with the browser.

    Raises:
        AssertionError: If the page title does not contain "Python" or if no search results are found.
    """
    driver.get("http://www.python.org")
    assert "Python" in driver.title
    elem = driver.find_element(By.NAME, "q")
    elem.clear()
    elem.send_keys("pycon")
    elem.send_keys(Keys.RETURN)
    assert "No results found." not in driver.page_source


def test_wikipedia_search(driver):
    """
    Tests the Wikipedia search functionality by searching for the term "DevOps".
    This function navigates to the Wikipedia homepage, performs a search for 
    the term "DevOps", and verifies that the resulting page contains the correct 
    heading and title.
    Args:
        driver (WebDriver): The Selenium WebDriver instance used to interact 
                            with the browser.
    Steps:
        1. Navigate to the Wikipedia homepage.
        2. Locate the search input field and enter the term "DevOps".
        3. Submit the search query.
        4. Wait for the search results page to load and verify the heading.
        5. Assert that the page title and heading match the search term.
    Raises:
        AssertionError: If the heading or title does not match the expected value.
    """
    driver.get("https://www.wikipedia.org/")

    search_input = driver.find_element(By.ID, "searchInput")

    search_input.send_keys("DevOps")

    search_input.send_keys(Keys.RETURN)

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "firstHeading"))
    )

    heading = driver.find_element(By.ID, "firstHeading")
    print(f"Page heading is: {heading.text}")

    assert "DevOps" in heading.text, "Search failed or wrong page loaded."

    print("Page title after search:", driver.title)
    element = driver.find_element(By.CLASS_NAME, "mw-page-title-main")
    assert element.text == "DevOps"