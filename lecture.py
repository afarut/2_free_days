from cmath import log
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from time import sleep
import requests
from config import NAME, logger, API_KEY
import sys





def go_to_lecture(link):
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("user-data-dir=./chromeprofile")
    options.add_argument('--disable-extensions')
    options.add_argument("--incognito")
    options.add_argument("--disable-plugins-discovery")
    options.add_argument("--start-maximized")
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            const newProto = navigator.__proto__
            delete newProto.webdriver
            navigator.__proto__ = newProto
            """
        })

    driver.get(link)
    logger.info(f"Go to {link}")
    try:
        wait_driver = WebDriverWait(driver, 8)
        wait_driver.until(expected_conditions.presence_of_element_located((By.ID, "name")))
        logger.info("It worked!")
    except TimeoutException:
        logger.critical("Timeout happened no page load")
        sys.exit()

    sleep(2)
    name_input = driver.find_element(By.ID, 'name')
    name_input.clear()
    name_input.send_keys(NAME)
    logger.info("Go to lecture")
    sleep(1.5)
    driver.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div/div/div[4]/input').click()
    try:
        try:
            wait_driver = WebDriverWait(driver, 8)
            wait_driver.until(expected_conditions.presence_of_element_located((By.XPATH, "/html/body/div/div/div/main/div[1]/div[1]/h3/span")))
        except TimeoutException:
            logger.critical("Timeout happened no page load")
            sys.exit()


        title = driver.find_element(By.XPATH, "/html/body/div/div/div/main/div[1]/div[1]/h3/span").text
        text = f"Вы присоединились к встрече с названием: {title}"
        logger.info(f"Welcome to {title}")
        requests.post(f"https://api.telegram.org/bot{API_KEY}/sendMessage", 
            data={"text": f"Welcome to {title}, {NAME}", "chat_id": 705853549})
        sleep(5400)
    except Exception as e: # For all errors
        logger.error(e)
    driver.quit()
    logger.info("The lecture is over")
