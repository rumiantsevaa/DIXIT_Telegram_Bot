import os
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

USERNAME = os.getenv("PA_USERNAME")
PASSWORD = os.getenv("PA_PASSWORD")

def wait_and_click(driver, by, value, timeout=10):
    for _ in range(timeout * 2):
        try:
            driver.find_element(by, value).click()
            return
        except:
            time.sleep(0.5)
    raise Exception(f"Element not found: {value}")

def wait_and_type(driver, by, value, text, timeout=10):
    for _ in range(timeout * 2):
        try:
            el = driver.find_element(by, value)
            el.clear()
            el.send_keys(text)
            return
        except:
            time.sleep(0.5)
    raise Exception(f"Field not found: {value}")

def run():
    options = uc.ChromeOptions()
    options.headless = True
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = uc.Chrome(options=options)
    driver.get("https://www.pythonanywhere.com/login/")

    wait_and_type(driver, By.ID, "id_auth-username", USERNAME)
    wait_and_type(driver, By.ID, "id_auth-password", PASSWORD)
    wait_and_click(driver, By.ID, "id_next")
    time.sleep(3)


    driver.get(f"https://www.pythonanywhere.com/user/{USERNAME}/consoles/")
    time.sleep(3)
    close_buttons = driver.find_elements(By.CSS_SELECTOR, 'span.glyphicon-remove')
    for btn in close_buttons:
        try:
            btn.click()
            time.sleep(1)
        except:
            pass

    driver.get(f"https://www.pythonanywhere.com/user/{USERNAME}/files/home/{USERNAME}")
    time.sleep(2)
    open_link = driver.find_element(By.CSS_SELECTOR, f'a[href="/user/{USERNAME}/consoles/bash//home/{USERNAME}/new"]')
    open_link.click()
    time.sleep(10)

    
    driver.switch_to.frame(driver.find_element(By.ID, "id_console"))
    time.sleep(5)
    
    body = driver.find_element(By.TAG_NAME, "body")
    actions = ActionChains(driver)
    actions.move_to_element(body).click()
    actions.send_keys('python3 pythonanywhere_starter.py')
    actions.send_keys(Keys.ENTER)
    actions.perform()
    driver.quit()


run()
