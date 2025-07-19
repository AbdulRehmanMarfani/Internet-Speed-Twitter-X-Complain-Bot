import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# Load environment variables
load_dotenv()

PROMISED_DOWN = int(os.getenv("PROMISED_DOWN"))
PROMISED_UP = int(os.getenv("PROMISED_UP"))
EDGE_DRIVER_PATH = os.getenv("EDGE_DRIVER_PATH")
X_EMAIL = os.getenv("X_EMAIL")
X_PASSWORD = os.getenv("X_PASSWORD")
X_USERNAME = os.getenv("X_USERNAME")
SPEEDTEST_URL = "https://www.speedtest.net/"

def create_driver():
    options = Options()
    return webdriver.Edge(service=Service(EDGE_DRIVER_PATH), options=options)

def get_speed(elem):
    for _ in range(90):
        try:
            speed = float(elem.get_attribute("textContent"))
            return speed
        except ValueError:
            time.sleep(1)
    raise Exception("Speed test did not finish in time.")

def test_internet_speed():
    driver = create_driver()
    driver.get(SPEEDTEST_URL)
    driver.maximize_window()

    try:
        accept_cookies = driver.find_element(By.XPATH, "//button[contains(text(), 'Accept')]")
        accept_cookies.click()
    except:
        pass

    driver.find_element(By.CLASS_NAME, "js-start-test").click()

    wait = WebDriverWait(driver, 90)
    download_elem = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "download-speed")))
    upload_elem = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "upload-speed")))

    download_speed = get_speed(download_elem)
    upload_speed = get_speed(upload_elem)

    print(f"Download Speed: {download_speed} Mbps")
    print(f"Upload Speed: {upload_speed} Mbps")

    driver.quit()
    return download_speed, upload_speed

def tweet(download_speed, upload_speed):
    driver = create_driver()
    driver.get("https://x.com/login")
    driver.maximize_window()

    try:
        email_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//input[@autocomplete='username']"))
        )
        email_input.send_keys(X_EMAIL)
        email_input.send_keys(Keys.RETURN)
        time.sleep(2)

        try:
            username_input = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//input[@name='text']"))
            )
            username_input.send_keys(X_USERNAME)
            username_input.send_keys(Keys.RETURN)
            time.sleep(2)
        except:
            pass

        password_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='password']"))
        )
        password_input.send_keys(X_PASSWORD)
        password_input.send_keys(Keys.RETURN)
        time.sleep(7)

        tweet_box = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[@data-testid='tweetTextarea_0']"))
        )
        tweet_box.click()
        ActionChains(driver).move_to_element(tweet_box).click().send_keys(" ").perform()
        tweet_box.send_keys(
            f"My internet is running at {download_speed} Mbps down / {upload_speed} Mbps up. "
            f"Really? I pay for {PROMISED_DOWN} / {PROMISED_UP}. #SpeedTest"
        )
        time.sleep(2)

        tweet_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='tweetButtonInline']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", tweet_button)
        tweet_button.click()
        time.sleep(2)
        print("Tweet posted successfully.")
    except Exception as e:
        print("Error while tweeting:", e)
    finally:
        driver.quit()

def safe_action(action, retries=3):
    for attempt in range(retries):
        try:
            return action()
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(2)
    raise Exception("All retries failed.")

def main():
    download_speed, upload_speed = safe_action(test_internet_speed)
    if download_speed < PROMISED_DOWN or upload_speed < PROMISED_UP:
        safe_action(lambda: tweet(download_speed, upload_speed))
    else:
        print("Internet speed is as promised. No tweet necessary.")

if __name__ == "__main__":
    main()
