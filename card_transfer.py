"""
Python BOT for transfering cards to main account using Peakmonsters
"""
import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

print("\nSCIDU - BOT para envio de cartas em lote via PeakMonsters\n")


def loadAccounts():
    load_dotenv()
    userlst = os.getenv("ACCUSERNAME").split(",")
    postinglst = os.getenv("POSTING_KEY").split(",")
    activelst = os.getenv("ACTIVE_KEY").split(",")
    pwlst = list(zip(postinglst, activelst))
    print(str(len(userlst)) + " accounts loaded!\n")
    print(userlst)
    return dict(zip(userlst, pwlst))


def startBrowser():
    options = Options()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    return webdriver.Chrome(options=options, executable_path="chromedriver.exe")


def main():
    # Load accounts
    acc_dict = loadAccounts()

    # Loop trough accounts
    for user, pw_lst in acc_dict.items():
        # Starts Chrome WebDriver
        driver = startBrowser()

        # Define standard wait
        wait = WebDriverWait(driver, 30)

        # Prints current account
        print(user)

        # Open Peakmonsters website
        driver.get("https://peakmonsters.com/")

        # Log in using username and posting key
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="app"]/div[5]/div/div[3]/div/button')))
        driver.find_element(
            By.XPATH, '//*[@id="app"]/div[5]/div/div[3]/div/button').click()
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//a[normalize-space()='Login']")))
        driver.find_element(By.XPATH, "//a[normalize-space()='Login']").click()
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//input[@placeholder='Email / Username']")))
        elm_user = driver.find_element(
            By.XPATH, "//input[@placeholder='Email / Username']")
        elm_user.clear()
        elm_user.send_keys(user)
        elm_pw = driver.find_element(
            By.XPATH, "//input[@placeholder='Password / Posting Key']")
        elm_pw.clear()
        elm_pw.send_keys(pw_lst[0])
        driver.find_element(By.XPATH, "//img[@alt='Login']").click()

        # Go to My Cards section
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//a[normalize-space()='My Cards']")))
        driver.find_element(
            By.XPATH, "//a[normalize-space()='My Cards']").click()

        # Select only owned cards
        driver.find_element(By.XPATH, "//li[37]/a/div[1]/input").click()

        time.sleep(2)

        # Counts owned cards
        cards_rows = len(driver.find_elements_by_xpath("//tbody/tr"))

        # Check if have zero owned cards
        if cards_rows == 0:
            print("Account doens't seem to have any cards owned!")
            driver.close()
            continue

        # Print names of cards to log #TODO: Proper naming formatting
        for i in range(cards_rows):
            card = driver.find_element(
                By.XPATH, "//tbody/tr[" + str(i + 1) + "]/td[2]/div/div")

            card_name = card.text.split()[:2]
            card_frame = driver.find_element(
                By.XPATH, "//tbody/tr[" + str(i + 1) + "]/td[2]/div/a/div")

            classes = card_frame.get_attribute('class')

            if "monster-img-gold" in classes:
                print(card_name)
                print("Gold")
            else:
                print(card_name)

        # Click to Select all cards
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//table/thead/tr/th[1]/a/i")))
        driver.execute_script("window.scrollTo(0, 0)") # TODO: Test without on Headless
        driver.find_element(By.XPATH, "//table/thead/tr/th[1]/a/i").click()

        # Go to transfer card screen
        driver.find_element(By.XPATH, "//i[@class='icon-stack3']").click()

        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[normalize-space()='Transfer']")))
        driver.find_element(By.XPATH,
                            "//button[normalize-space()='Transfer']").click()

        # Fill transfer with main account and continues
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//input[@placeholder='Account Name']")))
        elm_main_acc = driver.find_element(By.XPATH,
                                           "//input[@placeholder='Account Name']")
        elm_main_acc.clear()
        elm_main_acc.send_keys(os.getenv("MAIN_ACC"))

        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[@class='btn btn-success btn-xs']")))
        driver.find_element(By.XPATH,
                            "//button[@class='btn btn-success btn-xs']").click()
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[@class='sweet-modal theme-light has-title has-content is-visible']//button[@class='btn btn-primary btn-xs'][normalize-space()='Confirm']")))
        driver.find_element(By.XPATH,
                            "//div[@class='sweet-modal theme-light has-title has-content is-visible']//button[@class='btn btn-primary btn-xs'][normalize-space()='Confirm']").click()

        time.sleep(3)

        # Clicks Continue on HiveSigner
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//a[normalize-space()='Continue']")))
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);") # TODO: Test without on Headless
        driver.find_element(
            By.XPATH, "//a[normalize-space()='Continue']").click()

        # Log in on HiveSigner using Active Key
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//input[@id='username']")))
        elm_hive_login = driver.find_element(By.XPATH,
                                             "//input[@id='username']")
        elm_hive_login.clear()
        elm_hive_login.send_keys(user)

        elm_hive_pw = driver.find_element(By.XPATH, "//input[@id='password']")
        elm_hive_pw.clear()
        elm_hive_pw.send_keys(pw_lst[1])

        driver.find_element(
            By.XPATH, "//span[@class='checkbox mr-2 -checked']").click()

        driver.find_element(
            By.XPATH, "//button[normalize-space()='Login']").click()

        time.sleep(3)
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[normalize-space()='Approve']")))
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);") # TODO: Test without on Headless
        driver.find_element(
            By.XPATH, "//button[normalize-space()='Approve']").click()

        time.sleep(5)

        driver.close()


if __name__ == "__main__":
    main()
