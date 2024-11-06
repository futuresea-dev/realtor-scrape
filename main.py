from seleniumbase import Driver
from selenium.webdriver.common.by import By
import csv
import re
import argparse
import math


def parse_arguments():
    """
    Parse command-line arguments for the Realtor.com agent data scraper.

    This function sets up the argument parser and defines the required
    command-line arguments for the scraper.

    Returns:
        argparse.Namespace: An object containing the parsed arguments.
            - origin_link (str): The URL of the real estate agents page to scrape.

    Raises:
        SystemExit: If the required arguments are not provided or are invalid.
    """
    parser = argparse.ArgumentParser(description='Scrape Realtor.com agent data.')
    parser.add_argument('origin_link', type=str, help='The URL of the real estate agents page to scrape.')
    return parser.parse_args()


def extract_number_of_realtors(driver):
    """
        Extracts the number of REALTORS® found from the search result page.

        This function searches for a specific pattern in the text of the search result element
        to find the total number of REALTORS® listed.

        Args:
            driver (selenium.webdriver.remote.webdriver.WebDriver): The Selenium WebDriver instance
                used to interact with the web page.

        Returns:
            int: The number of REALTORS® found. Returns 0 if no number is found in the search result text.

    """
    result_elm = driver.find_element(By.CLASS_NAME, "search-result")
    result_txt = result_elm.text
    pattern = r'\b(\d+)\s+REALTORS®\s+found'
    match = re.search(pattern, result_txt)
    if match:
        number_found = int(match.group(1))
        print(f'Extracted number: {number_found}')
        return number_found
    print('No number found')
    return 0


def extract_phone_numbers(agent_link, driver):
    """
    Extract up to two phone numbers from an agent's link element.

    This function attempts to find phone numbers associated with a real estate agent
    from their listing on a web page. It looks for elements with the class name "agent-phone"
    and extracts the text content. If no text is directly available, it uses JavaScript to
    retrieve the inner text.

    Args:
        agent_link (selenium.webdriver.remote.webelement.WebElement): The WebElement representing
            the agent's listing on the page.
        driver (selenium.webdriver.remote.webdriver.WebDriver): The Selenium WebDriver instance
            used to execute JavaScript if needed.

    Returns:
        list: A list containing up to two phone numbers as strings. If fewer than two numbers
        are found, the list is padded with empty strings to always return a list of length 2.

    """
    phone_elements = agent_link.find_elements(By.CLASS_NAME, "agent-phone")
    phone_numbers = []
    for phone_element in phone_elements:
        phone_number = phone_element.text or driver.execute_script("return arguments[0].innerText;", phone_element)
        if phone_number:
            phone_numbers.append(phone_number)
    return phone_numbers[:2] + [''] * (2 - len(phone_numbers))


def scrape_agent_data(agent_link, driver):
    """
        Scrape relevant data for a single real estate agent from their listing on a web page.

        This function extracts the agent's name, business name, phone numbers, and profile link
        from the provided agent listing element.

        Args:
            agent_link (selenium.webdriver.remote.webelement.WebElement): The WebElement representing
                the agent's listing on the page.
            driver (selenium.webdriver.remote.webdriver.WebDriver): The Selenium WebDriver instance
                used to interact with the web page and execute any necessary JavaScript.

        Returns:
            list: A list containing the scraped agent data in the following order:
                [name, business name, primary phone number, secondary phone number, profile link]
                Where:
                - name (str): The agent's full name with commas replaced by spaces.
                - business name (str): The name of the agent's agency or group, with commas and quotes removed.
                - primary phone number (str): The first phone number found for the agent, if any.
                - secondary phone number (str): The second phone number found for the agent, if any.
                - profile link (str): The URL of the agent's profile page.
    """
    name = agent_link.find_element(By.CLASS_NAME, "agent-name").text.replace(",", " ").replace('"', "").replace("\n", "")
    bus_name = agent_link.find_element(By.CLASS_NAME, "agent-group").text.replace(",", " ").replace('"', "").replace("\n", "")
    phone_1, phone_2 = extract_phone_numbers(agent_link, driver)
    link_addr = agent_link.find_element(By.CSS_SELECTOR, '[aria-label="link name"]')
    href_value = link_addr.get_attribute('href')
    return [name, bus_name, phone_1, phone_2, href_value]


def main():
    """
        Execute the main scraping process for Realtor.com agent data.

        This function orchestrates the entire scraping process, including:
        1. Parsing command-line arguments
        2. Setting up the CSV file for output
        3. Initializing the web driver
        4. Extracting the total number of realtors
        5. Iterating through pages of realtor listings
        6. Scraping individual agent data
        7. Writing the data to the CSV file

        The function doesn't take any parameters as it uses command-line arguments
        parsed by the parse_arguments() function.

        Returns:
            None

        Side effects:
            - Creates or overwrites a file named 'output.csv' with scraped agent data
            - Prints progress information to the console
    """
    args = parse_arguments()
    header = ["name", "Agency", "Phone Number 1", "Phone Number 2", "Address"]

    with open('output.csv', 'w', newline='') as file:
        csv.writer(file).writerow(header)

    driver = Driver(uc=True)
    driver.get(url=args.origin_link)
    number_found = extract_number_of_realtors(driver)
    driver.quit()
    if number_found:
        total_pages = math.ceil(number_found / 20)
        for page_id in range(1, total_pages + 1):
            url = f'{args.origin_link}/pg-{page_id}'
            driver = Driver(uc=True)
            driver.get(url)
            link_list = driver.find_elements(By.XPATH, '//*[@data-testid="component-agentCard"]')

            with open('output.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                for agent_link in link_list:
                    agent_data = scrape_agent_data(agent_link, driver)
                    writer.writerow(agent_data)
            driver.quit()

    driver.quit()


if __name__ == "__main__":
    main()

